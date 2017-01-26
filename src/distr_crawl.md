## Distributive Crawling

To speed up time-consuming crawling process, we can utilize multiple (slave) machines
to run crawler script at the same time.
At the end of day, use `rsync` command to collect and push all the updated corpus
files from these machines to a single remote server.
The server, runs indexer regularly to re-index the entire corpus collected from slave
machines, after which the server will switch to new index, and delete the old index.
On the other hand, slave machines loop continuously, keep crawling a range of pages
forever.
In this easy model, we can avoid complicated index update/delete operations (in fact,
these operations are not supported currently in our indexer), while at the same time
achieve updated search engine index.

Here records things you need to do in order to operate under this model.

### 0. Install rsync
Install using apt (assuming on Ubuntu):
```sh
$ sudo apt-get install rsync
```

### 1. Server side
Create a rsync config file at `/etc/rsyncd.conf`, below is an example:
```
hosts allow = 202.98.77.20, 127.0.0.1

uid = root
gid = root
port = 8990

use chroot = no
max connections = 4
syslog facility = local5

pid file  = /root/rsyncd.pid
lock file = /root/rsyncd.lock
log file  = /root/rsyncd.log

[corpus]
	read only = no
	list = yes
	path = /root/corpus
	comment = rick and mody
```

Start rsync daemon:
```sh
$ sudo rsync --daemon --config=/etc/rsyncd.conf
```

To stop rsync daemon:
```
$ sudo kill -INT `cat /root/rsyncd.pid`
```

### 2. Slave-machine side
Test connection by listing remote directory:
```sh
$ rsync rsync://138.68.58.236:8990/corpus
```

Then use the following command to push local corpus files to remote server
(this is incremental updates, so no worry it would delete any remote file)
```sh
$ rsync -zauv --exclude='*.html' --progress corpus/ rsync://138.68.58.236:8990/corpus --bwlimit=600
```
`-z` option compresses the transferring data, `-a` option forces recursive search on
source directory, `-u` option does update only when local file is newer, `--bwlimit` specifies
bandwidth maximum usage, and `-v` option verbalizes this process.

When using `crawler-math.stackexchange.com.py`
crawler script, you can specify a "hook script" for automatically doing rsync.
An example hook script for this purpose (i.e. `push-to-server.sh`) is located at
`demo/crawler`.
Also, you can specify `--patrol` to enable crawler script to also fetch recently active posts (besides most recently created).
This is useful when we are reguarly and repeatedly watching for updates of target Website:
```sh
$ cd $PROJECT/demo/crawler
$ ./crawler-math.stackexchange.com.py -b <begin page> -e <end page> --hook-script ./push-to-server.sh --patrol
```
(you may need to install `dnsutils` which contains `dig` command to be used in `push-to-server.sh`)
