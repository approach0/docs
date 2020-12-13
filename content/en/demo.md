## WEB Demo
The source code contains a complete WEB demo and webpage interface that
you can set up on your own machine.

### Install and config Nginx/PHP
Given Nginx on Ubuntu 16.04 LTS as example,
```sh
$ sudo apt-get install nginx php-fpm
```

check if `.sock` file exists
```
$ ls /run/php/php7.0-fpm.sock
```

edit config file
```
$ sudo vi /etc/nginx/sites-enabled/default
```

and uncomment php related lines:
```
 ...
	location ~ \.php$ {
		include snippets/fastcgi-php.conf;
		fastcgi_pass unix:/run/php/php7.0-fpm.sock;
	}
 ...
```

Restart php-fpm and nginx:
```
$ sudo /etc/init.d/php7.0-fpm restart
$ sudo systemctl restart nginx
```

Write a simple php file on `/var/www/html/test.php`
```
$ cat /var/www/html/test.php
<?php
echo 'hello world';
?>
```

Visit `http://127.0.0.1/test.php` to see if `hello world` is
printed. If it is not, a useful trick is to enable
display\_errors in php.inf
```
$ vi /etc/php/7.0/fpm/php.ini
```
and set `display_errors = On`, then restart php-fpm and nginx
to figure out what is going wrong.

### Link or copy WEB files
Now that php service is running, put our WEB source files to
HTTP root directory.

```sh
$ cd /var/www/html/
$ ln -s $PROJECT/demo/web ./demo
```
Make sure $PROJECT path is accessable by httpd (e.g. use `su www-data -s /bin/bash` to test permission), then
you should be able to visit `http://127.0.0.1/demo` page.

### Install php-curl
The `search-relay.php` in web directory is using php-curl to relay
search GET requests to searchd, the latter is running on port 8921 in
default. So make sure php-curl is installed.
```
$ sudo apt-get install php-curl
$ sudo systemctl restart nginx
```

### Run searchd in background

Install tmux for keeping searchd running in a detached session
(so that searchd can keep running even if we exit the shell).
```
$ sudo apt-get install tmux
$ cd $PROJECT/searchd
$ tmux new -d -s searchd_session './run/searchd.out -i ~/index'
```

At this point, you should be able to get search results back after
entering queries in demo page.

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

#### Drop external TCP traffic to searchd
```sh
iptables -A INPUT -i lo -j ACCEPT
iptables -A INPUT -p tcp --dport 8921 -j DROP
```
The first rules give full access to *localhost*, otherwise the second
rule blocks any packet sent to searchd port.
