## DevOps
Approach Zero operates based on containerized micro-services and Docker Swarm.
In particular, its DevOps uses a wrapper tool called [Calabash](https://github.com/approach0/calabash)
on top, to bootstrap on IaaS services, deploy and inspect logs.

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
with your own credentials/passwords (please also add a prefix `SECRET:` to these fields), then run job daemon
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

When you need to update remote configurations, or update Calabash service, just edit `config.toml` and run
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
Before one can run any calabash "job", one has to login to obtain a JWT token. You can do so by visiting `/auth/login` from `lattice` service test page to obtain an initial JWT token (with Long-live cookie radio box checked).

#### Bootstrap HTTPS gateway
In Calabash panel, label the node `dns_pin=true` and set your domain name DNS to point to this node IP address.

Once your DNS record is propagated (you can verify it using *ping* command), create service `gateway` with domain name argument:
```
swarm:service-create?service=gateway&domain_name=approach0.me
```

After `gateway` is deployed, you can test and visit `https://<your_domain_name>` to see if `gateway` service is working as expected.
If it all looks good, you may want to remove `gateway_bootstrap` service because it is no longer necessary. `gateway` service will automatically update
HTTPS certificates and take care of everything related to Let's Encrypt services.

If you hit [the rate limit](https://letsencrypt.org/docs/rate-limits/) of Let's Encrypt, go to [https://crt.sh/](https://crt.sh/) to find out your past issue history of that domain and estimate when you can get a new certificate again.

### 3. Setting Up
The rest of it is just clicking buttons, create new nodes, label them and setup new services until
Approach Zero cluster can automatically refresh its index and switch to new indices regularly.

However, the order of the services to boot up is important. Here is a recommended order to set up other services:

1. For the bootstrap node (namely `persistent` node), create:

    * `ui_login` for JWT login later

    * `ui_404` for 404 page redirection

    * `monitor` and `grafana` to start monitoring.
      Import Grafana configurations from JSON files (at `configs` directory)

    * `usersdb_syncd` for database rsync backup, listening on port `8873`.
      This service has to be on the same node with `usersdb` because they bind to the same on-disk volume

    * `corpus_syncd` for accepting coprus harvest from crawlers (listening on port `873`)
       `corpus_syncd` will also regularly output current corpus size and number of files,
       once it is deployed, you may want to use rsync to restore your previous backup corpus files.

    * `guide` and `docs` services for Approach Zero user guide and developer documentation page.
        These two services contain Github workflows to trigger webhooks to update their static HTML content.
        For webhooks to work, remember to modify the domain name to your own in their Github workflow files

    * `stats` for search engine query logs/statistics page

    * `ui_search` for search page UI (scale it to match the number of search nodes to load-balance large traffic)

2.  Create 4 "indexer" nodes for indexing and crawling, label each node a shard number from 1 to 4, then create:

    * `indexer` for indexers

    * and `index_syncd` for transmitting indices to new search nodes going to be created later.
       Watch `index_syncd` logs for the most recently created index image whose name contains its creation timestamp.

    * `feeder` service to start feeding current corpus files to indexers (if any)

3. Create 4 "searchd" nodes for search daemons, label each node a shard number from 1 to 4, then create:

    * `crawler_sync` for sending crawler coprus harvest to `corpus_syncd`.

    * `crawler` for deploying crawlers

    * Create `searchd:green` or `searchd:blue` services as SSH-exposed search instances responsible for different index sharding,
      the one running on the first shard will establish and listen at port 8921.
      (to support MPI replicas, we rename the service to "green" or "blue" for parallel search services, load-balancing or [blue/green deployment](https://bing.com/search?q=blue%2Fgreen+deployment))

    * `searchd_mpirun` for running those search instances using MPI protocol. For example, to target the "green" search instances, we can run job:

    ```
    swarm:service-create?service=searchd_mpirun:green_mpirun&target_serv=green
    ```
    By default, search daemons do not cache disk index into memory, this makes the daemon startup really fast, but the disadvantage is obvious, it hurts performance. To enable cache, one can run job with parameters like (numbers are in MB):
    ```
    swarm:service-create?service=searchd_mpirun:green_mpirun&target_serv=green&word_cache=100&math_cache=500 # for old nano-linode w/o container
    swarm:service-create?service=searchd_mpirun:green_mpirun&target_serv=green&word_cache=0&math_cache=256 # for new nano-linode w/ container
    ```
    After this point you may want to test yet-to-be-routed search service before completely switching to it (by creating `relay` service).
    We can test this search instance locally by
    ```sh
    $ docker run approach0/a0 test-query.sh http://<IP-of-shard-1-searchd>:8921/search /tmp/test-query.json
    ```

    * Create `relay` service to accept routed request from gateway and direct them to targeted search service (and also stats service APIs).

    ```
    swarm:service-create?service=relay:green_relay&relay_target=green
    ```
    One can test relay service by visiting `/search-relay/?q=hello`

    * (Optional) `ss` for HTTP(s) proxy service

#### A few notes

To set a different config entry, one can run a job with injected variable. For example:
```
swarm:service-create?service=indexer&service_indexer_mesh_sharding=5
```

Be careful of service dependency. For example, if you want restart `usersdb` service,
you will also need to restart `lattice` and `stats` services afterwards:
```
$ node cli/cli.js -j 'swarm:bootstrap-update?nodeIP=<IP>&port=8982&services=lattice,stats'
```

### 4. Maintenance

#### Update a service
A normal update has `--update-order=start-first` passed to Docker Swarm in Calabash, which means it will start a parallel service and switch to the new one (stop the old) once it is ready. Doing this also means an update on service will fail if existing old instance has already filled the only placement slot(s). In this case, you can choose to create a same service (instead of updating the service) because creating service in Calabash will also remove the old one.

#### Switch to a newer index
Switching to a newer index (usually when indices are updated) is essentially to repeat step 3 in above section. Except that
* You will need to remove old search related services (better to remove the `relay` service first for maximum availability) before deleting out-dated search nodes
* Non-search related services (such as `crawler` etc.) will be re-distributed after deleting out-dated search nodes, so no need to remove them
* One may also want to re-create `index_syncd` service to refresh mount point in container (so that `df -h` will print newly mounted loop device)

#### Restore and backup
Those rsync services are deployed to enable restore/backup files using rsync remotely, one can issue the following commands to test rsync daemon:
```sh
$ export RSYNC_PASSWORD=<your_rsync_password>
$ rsync rsync://rsyncclient@<your_IP>:<rsync_port>/
```

When restoring corpus data, be aware to add `--ignore-existing` to skip updating files that exist on receiver, for example:
```sh
$ rsync --ignore-existing -ravz ./corpus-2020/ rsync://rsyncclient@<IP>/data/tmp/
```

To backup corpus data, add `--update` option:
```sh
$ rsync --update -ravz rsync://rsyncclient@<IP>/data/tmp/ ./corpus-2020/
```

To backup/restore database data, use port `8873`. For example
```sh
$ rsync -v ./postgres-2020-12-07.dump rsync://rsyncclient@<IP>:8873/data/
```
and when restoring, you will also need to login to the server, `exec` into the `usersdb` container and run
```sh
$ ./entrypoint.sh clean_and_restore postgres-2020-12-07.dump
```
to reset database content to the uploaded dump.

#### Migrate data between hosts
One can also use rsync to migrate data form one host to another, but please ensure the syncd services are first re-distributed to the new host.
```sh
$ rsync -v /var/lib/docker/volumes/usersdb_vol/_data/*.dump rsync://rsyncclient@<IP>:8873/data/
$ rsync -ravz /var/lib/docker/volumes/corpus_vol/_data/tmp rsync://rsyncclient@<IP>:873/data/
```
Postgres database would not start successfully if you have a non-empty directory, so you will need to move database dump files to a temporal location
and then move back after service restarted.

After migration, run `swarm:bootstrap-refresh-id` job from local machine to enable ssh access to new remote node.

#### Switch to a new domain name
Before change the A record at your DNS provider, remove the data volumes related to gateway (e.g., `gateway_keys_vol`) and then replace `gateway` service.
This will force gateway to install and setup certificates for the new domain name.

You may also want to ensure `gateway_bootstrap` service is up and manipulate through the bootstrap gateway version to avoid interupt during gateway switching.

Use some DNS lookup utility to test DNS refresh:
```
$ drill approach0.xyz

;; ->>HEADER<<- opcode: QUERY, rcode: NOERROR, id: 7165
;; flags: qr rd ra ; QUERY: 1, ANSWER: 1, AUTHORITY: 2, ADDITIONAL: 4 
;; QUESTION SECTION:
;; approach0.xyz.       IN      A

;; ANSWER SECTION:
approach0.xyz.  600     IN      A       172.104.159.193

;; AUTHORITY SECTION:
approach0.xyz.  1800    IN      NS      dns2.registrar-servers.com.
approach0.xyz.  1800    IN      NS      dns1.registrar-servers.com.

;; ADDITIONAL SECTION:
dns1.registrar-servers.com.     1151    IN      A       156.154.132.200
dns2.registrar-servers.com.     1052    IN      A       156.154.133.200
dns1.registrar-servers.com.     310     IN      AAAA    2610:a1:1024::200
dns2.registrar-servers.com.     1520    IN      AAAA    2610:a1:1025::200

;; Query time: 2228 msec
;; SERVER: 202.96.128.166
;; WHEN: Mon Dec  7 12:03:25 2020
;; MSG SIZE  rcvd: 194
```

#### Shell login
At any time, you can login to the shell of a node using SSH or `mosh`:
```sh
$ mosh -ssh 'ssh -p 8982' <IP>
```
mosh is using UDP over SSH protocol, it is sometimes essential for fast global remote access.

To ask ssh daemon remember your local host, use `ssh-copy-id`:
```sh
$ ssh-copy-id -p 8982 root@<IP>
```

#### Quorum reset
If for some reason a quorum lost leader and ends up with a even number of managers, one needs 
to reset the quorum from one of its manager node:
```
$ docker swarm init --force-new-cluster
```
