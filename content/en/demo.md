## WEB Demo
A [separate repository](https://github.com/approach0/ui-approach0) contains a WEB front end to interact with search engine.
The front end uses a canonicalized string format to represent query, e.g., `NOT title:prove, AND body:$a^2+b^2=c^2$`.
This string gets encoded as URI parameters and sent to a relay service which listens at port 8080, the relay service then
parse the linear canonicalized string to structured JSON format that search engine daemon is easy to take as input.

### Local demo
To setup relay service locally, the easiest way is to utilize existing Docker images:
```sh
$ docker run -it --network bridge --mount type=volume,src=usersdb_vol,dst=/postgres/data -p 8081:80 -p 5432:5432 approach0/postgres13
$ docker run -it --network host approach0/a0-stats
$ docker run -it --network host -e A0_SEARCHD=localhost -p 8080:8080 approach0/a0-relay
```

Ensure a search daemon is running locally, then to view a local WEB demo, you only need to serve the WEB front end page:
```
$ git clone git@github.com:approach0/ui-approach0.git
$ cd ui-approach0 
$ npm run watch
```
and visit `http://localhost:19985` in your browser.

To quickly debug in a container, one trick is to bind mount the source file directly into container:
```
$ docker run -it --network host --mount type=bind,src=`pwd`,dst=/code a0-stats bash
```

### Remote demo
There is not many differences to setup a demo remotely (e.g., from a VPS).
But oftenly, you will need to run services remotely in a detached session so when you leave the SSH session,
you do not interrupt your service.

Install tmux for keeping searchd running in a detached session
(so that searchd can keep running even if we exit the shell).
```
$ sudo apt-get install tmux
$ cd $PROJECT/searchd
$ tmux new -d -s searchd_session './run/searchd.out -i ~/index'
```

To attach this search daemon session:
```
$ tmux list-sessions
$ tmux attach -t searchd_session
```

To see logs from this search daemon:
```
$ tmux capture-pane -pt searchd_session
```

### Security
Configurations below are mainly for security considerations.
It disallow direct interaction with search engine, so user has to make request via relay service
which is written in PHP and offers more robust interface when directly exposing to public.

#### Drop external TCP traffic to searchd
```sh
iptables -A INPUT -i lo -j ACCEPT
iptables -A INPUT -p tcp --dport 8921 -j DROP
```
The first rules give full access to *localhost*, otherwise the second
rule may block any packet sent to searchd port.
