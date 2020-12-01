## DevOps
Approach Zero operates based on containerized micro-services and Docker Swarm.
In particular, its DevOps uses a wrapper tool called [Calabash](https://github.com/approach0/calabash)
on top of these to bootstrap on IaaS services, deploy and inspect logs.

### 1. CI/CD
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

### 2. Bootstrap

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

Use a node with at least 50 GB disk space (here Linode config-1) as the first node to bootstrap the cluster:
```sh
$ node cli/cli.js -j 'swarm:bootstrap?node_usage=persistent&iaascfg=linode_config_2'
```

Notice that sometimes it is helpful to test service locally before deployment, in these cases, run
```sh
$ node cli/cli.js -j 'swarm:bootstrap_localmock?node_usage=searchd&services=nil' # just to add additional node labels
$ node cli/cli.js -j 'swarm:bootstrap_localmock?node_usage=host_persistent&services=gateway_bootstrap,ui_search'
```

After bootstrap, you should be able to visit the Calabash panel via `http://<whatever_IP_assigned>:8080/backend` (served by `gateway_bootstrap` service with port is **8080**).

At any time, you can login to the shell of a node using SSH or `mosh`:
```sh
$ mosh -ssh 'ssh -p 8982' <IP>
```
mosh is using UDP over SSH protocol, it is sometimes essential for fast global remote access.

Also, after bootstrap, when you need to update remote configurations, or update Calabash service, just edit `config.toml` and run
```sh
$ node cli/cli.js -j 'swarm:bootstrap-update?nodeIP=<your_bootstrap_node_IP>&port=<your_bootstrap_node_SSH_port>&services=calabash'
```
Similarly, when you want to update any other "core" services that Calabash depends on (so that you cannot simply control Calabash to update them remotely),
just pass comma-separated list of service(s) you want to update like below
```sh
$ node cli/cli.js -j 'swarm:bootstrap-update?nodeIP=<your_bootstrap_node_IP>&port=<your_bootstrap_node_SSH_port>&services=calabash,gateway'
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

If you hit [the rate limit](https://letsencrypt.org/docs/rate-limits/) of Let's Encrypt, go to [https://crt.sh/](https://crt.sh/) to find out your past issue history of that domain and estimate when you can get a new certificate again.

### 3. Setting Up
The rest of it is just clicking buttons, create new nodes, label them and setup new services until
Approach Zero cluster can automatically refresh its index and switch to new indices regularly.

However, the order of the services to boot up is important. Here is a recommended order to set up other services:

1. For the bootstrap node (namely `persistent` node), create:
  1. `ui_login` for JWT login later
  2. `ui_404` for 404 page redirection
  3. `monitor` and `grafana` to start monitoring.
      Import Grafana configurations from JSON files (at `configs` directory)
  4.  `usersdb_syncd` for database rsync backup, listening on port `8873`.
      This service has to be on the same node with `usersdb` because they bind to the same on-disk volume
  5. `corpus_syncd` for accepting coprus harvest from crawlers (listening on port `873`)
     `corpus_syncd` will also regularly output current corpus size and number of files,
     once it is deployed, you may want to use rsync to restore your previous backup corpus files.
  6. `guide` and `docs` services for Approach Zero user guide and developer documentation page.
      These two services contain Github workflows to trigger webhooks to update their static HTML content.
      For webhooks to work, remember to modify the domain name to your own in their Github workflow files
  7. `stats` for search engine query logs/statistics page
  8. `feeder` service to start feeding current corpus files to indexers (if any)
2.  Create 4 "indexer" nodes for indexing and crawling, label each node a shard number from 1 to 4, then create:
  1. `indexer` for indexers
  2. and `index_syncd` for transmitting indices to new search nodes going to be created later.
     Watch `index_syncd` logs for the most recently created index image whose name contains its creation timestamp.
3. Create 4 "searchd" nodes for search daemons, label each node a shard number from 1 to 4, then create:
  1. `crawler_sync` for sending crawler coprus harvest to `corpus_syncd`.
  2. `crawler` for deploying crawlers
  3. `ui_search` for search page UI (scale it to match the number of search nodes to load-balance large traffic)
  4. Create `searchd:green` or `searchd:blue` services as SSH-exposed search instances responsible for different index sharding,
    the one running on the first shard will establish and listen at port 8921.
    (to support MPI replicas, we rename the service to "green" or "blue" for parallel search services, load-balancing or [blue/green deployment](https://bing.com/search?q=blue%2Fgreen+deployment))
  5. `searchd_mpirun` for running those search instances using MPI protocol. For example, to target the "green" search instances, we can run job:
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
  6. Create `relay-blue` or `relay-green` service to accept routed request from gateway and proxy them to corresponding search service (and also stats service APIs).
    One can test `relay-*` service by visiting `/search-relay/?q=hello`
  7. (Optional) `ss` for HTTP(s) proxy service

### 4. Maintenance

#### Update a service
A normal update has `--update-order=start-first` passed to Docker Swarm in Calabash, which means it will start a parallel service and switch to the new one (stop the old) once it is ready. Doing this also means an update on service will fail if the existing old instance has already filled the only replacement slot, in this case, you can choose to create a same service (instead of updating the service) because creating service in Calabash will also remove the old one.

### Rsync
Those rsync services are deployed to enable upload/backup files using rsync remotely, one can issue the following commands to test rsync daemon:
```sh
$ export RSYNC_PASSWORD=<your_rsync_password>
$ rsync rsync://rsyncclient@<your_IP>:<rsync_port>/
```

Use rsync from local host to backup/restore data accordingly.
