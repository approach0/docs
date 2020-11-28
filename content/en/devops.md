## DevOps
Approach Zero operates based on containerized micro-services and Docker Swarm.
In particular, its DevOps uses a wrapper tool called [Calabash](https://github.com/approach0/calabash)
on top of these to bootstrap on IaaS services, deploy and inspect logs.

### CI/CD
Github Actions is used for Approach Zero CI/CD, usually each code repository of the project has a `deploy` branch
which you can push to and trigger Github workflows, for example, to invoke webhooks, build and push Docker images to different Docker registry providers.

Those workflows are defined in `.github/workflows` directory of each repository.

On Github, across the [approach0 organization](https://github.com/organizations/approach0), we have created several [secrets](https://github.com/organizations/approach0/settings/secrets/actions) necessary for CI/CD jobs, including

* `DOCKERHUBPASSWORD`: Password for DockerHub registry
* `UCLOUDUSERNAME` and `UCLOUDPASSWORD`: Credentials for UHub registry
* `WEBHOOKSECRET` for documentation webhooks (triggered to re-generate documentation static pages on push events)
* `GITHUBPAT`: An open "PAT" with minimal permissions used by `ui_calabash` service to check Github workflows status

A completely independent cluster can be deployed for integration test.
Instead of automatically update service on code changes, we currently need to manually update service.

### Bootstrap

#### Bootstrap core services
To bootstrap a new cluster, fetch Calabash code
```sh
$ git clone git@github.com:approach0/calabash.git && cd calabash
```

Copy `config.template.toml` to a new file `config.toml` in the directory, edit `config.toml` and fill in the blanks (indicated by `___`)
with your own credentials/passwords and change the `domain_name` entry in `environment` to your own, then run job daemon
```sh
$ node ./jobd/jobd.js --config ./config.toml --no-looptask
```

Make sure cloud provider CLI image exists:
```sh
$ docker pull approach0/linode-cli
# Alternatively,
$ docker tag other-registry/username/linode-cli approach0/linode-cli
```

Use a node with at least 25 GB disk space (here Linode config-1) as the first node to bootstrap the cluster:
```sh
$ node cli/cli.js -j 'swarm:bootstrap?node_usage=persistent&iaascfg=linode_config_1'
```

After bootstrap, you should be able to visit the Calabash panel via `http://<whatever_IP_assigned>:8080/backend` (served by `gateway_bootstrap` service)

At any time, you can login to the shell of a node using SSH or `mosh`:
```sh
$ mosh -ssh 'ssh -p 8982' <IP>
```
mosh is using UDP over SSH protocol, it is sometimes essential for fast global remote access.

Also, after bootstrap, when you need to update remote configurations, or update Calabash service, just edit `config.toml` and run
```sh
$ node cli.js -j 'swarm:bootstrap-update?nodeIP=<your_bootstrap_node_IP>&port=<your_bootstrap_node_SSH_port>&services=calabash'
```
Similarly, when you want to update any other "core" services that Calabash depends on (so that you cannot simply control Calabash to update them remotely),
just pass comma-separated list of service(s) you want to update like below
```sh
$ node cli.js -j 'swarm:bootstrap-update?nodeIP=<your_bootstrap_node_IP>&port=<your_bootstrap_node_SSH_port>&services=calabash,gateway'
```

#### Bootstrap login

With Calabash panel, you can manipulate Docker Swarm easily and excute tasks written in shell scripts.
Before one can run any calabash "job", one have to login to obtain a JWT token. You can do so by visiting `/auth/login` from `lattice` service test page to obtain an initial JWT token (with Long-live cookie radio box checked).

#### Bootstrap HTTPS gateway
In Calabash panel, label the node `dns_pin=true` and set your domain name DNS to point to this node IP address.

Once your DNS record is propagated (you can verify it using *ping* command), create service `gateway`.

After `gateway` is deployed, you can test and visit `https://<your_domain_name>` to see if `gateway` service is working as expected.
If it all looks good, you may want to remove `gateway_bootstrap` service because it is no longer necessary. `gateway` service will automatically update
HTTPS certificates and take care of everything related to Let's Encrypt services.

### Setting Up
The rest of it is just clicking buttons, create new nodes, label them and setup new services until
Approach Zero cluster can automatically refresh its index and switch to new indices regularly.

However, the order of the services to boot up is important. Here is a recommended order to set up other services:

1. Create `ui_login` service for later JWT login
2. `monitor` and `grafana` services to start monitoring and import Grafana configurations from JSON files (at `configs` directory)
3. `usersdb_syncd` for database rsync service listening on port 8873
   (this service has to be on the same node with `usersdb` because they bind to the same on-disk volume)
4. `guide` and `docs` services for Approach Zero user guide and developer documentation page. These two services contain Github workflows to trigger
   webhooks to update their static HTML content. For webhooks to work, remember to modify the domain name to your own in their Github workflow files
5. `stats` service for search engine query logs and statistics webpage
6. Create 4 "indexer" nodes for indexing and crawling, label each node a shard number from 1 to 4
7. Deploy `corpus_syncd` and `crawler` services for corpus rsync (on port 873 of shard-1) and crawlers,
   `corpus_syncd` will also regularly output current corpus size and number of files.
   Once they are deployed, you may want to use rsync to restore your previous backup corpus files
8. `indexer` and `index_syncd` for indexers and transmitting indices to new search nodes 
   (you can watch `index_syncd` logs for the most recently created index image whose name contains its creation timestamp)
9. Then create `feeder` service to start feeding current corpus files to indexers
10. Create 4 "searchd" nodes for search daemons, label each node a shard number from 1 to 4
11. Create `searchd:green` services as SSH-exposed search instances responsible for different index sharding,
    the one running on the first shard will establish and listen at port 8921.
    (to support MPI replicas, we name the service "green" so that later we can add parallel search services, e.g., "blue" for load-balancing or [blue/green deployment](https://bing.com/search?q=blue%2Fgreen+deployment))
12. `searchd_mpirun` for running those search instances using MPI protocol. To target the "blue" search instances, run job:
    ```
    swarm:service-create?service=searchd_mpirun&target_serv=green
    ```
    By default, search daemons do not cache disk index into memory, this makes the daemon startup really fast, but the disadvantage is obvious, it hurts performance. To enable cache, one can run job with parameters like (numbers are in MB):
    ```
    swarm:service-create?service=searchd_mpirun&target_serv=green&word_cache=100&math_cache=500
    ```
    After this point you may want to test yet-to-be-routed search service before completely switching to it (by creating `relay` service).
    We can test this search instance locally by
    ```sh
    $ docker run approach0/a0 test-query.sh http://<IP-of-shard-1-searchd>:8921/search /tmp/test-query.json
    ```
13. Finally, create `relay` service to accept routed request from gateway and proxy them to search daemons (and also stats service APIs).
    One can test `relay` service by visiting `/search-relay/?q=hello`.

Those rsync services are deployed to enable upload/backup files using rsync remotely, one can issue the following commands to test rsync daemon:
```sh
$ export RSYNC_PASSWORD=<your_rsync_password>
$ rsync rsync://rsyncclient@<your_IP>:<rsync_port>/
```
