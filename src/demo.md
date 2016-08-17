## Setting up WEB Demo
The source code contains a complete WEB demo (also is the one
hosted on [our demo page](https://approach0.xyz/demo/)) that
you can set up on your own machine.

### Install and config Nginx/PHP
For convenience, here list steps to install a HTTP service
(given Nginx as example) that will accepts client AJAX request
from 80 port and use a php script to relay this request to
a running searchd program.

For Ubuntu 16.04 LTS,
```sh
$ sudo apt-get install nginx php-fpm
```

Check if `.sock` file exists
```
$ ls /run/php/php7.0-fpm.sock
```

Edit config file
```
$ sudo vi /etc/nginx/sites-enabled/default
```

Uncomment php related lines:
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
and set `display_errors = On`. Then restart php-fpm and nginx
again to figure out what is going wrong.

### Link or copy WEB files
Now that php service is running, put our WEB source files to
HTTP root directory.

```sh
$ cd /var/www/html/
$ ln -s $PROJECT/demo/web ./demo
```

Then you should be able to visit `http://127.0.0.1/demo` page.

### Install php-curl
The `search-relay.php` in web directory is using php-curl to relay
requests from 80 to searchd, the latter is running on port 8921 in
default. So make sure php-curl is installed.
```
$ sudo apt-get install php-curl
$ sudo systemctl restart nginx
```

(the searchd binding port is hard-coded, so is the port in
search-relay.php, currently if you want to modify this port number,
edit `searchd/config.h` and `demo/web/search-relay.php` and then
rebuild searchd)

### Run searchd in background

Install tmux for keeping searchd running in a detached session
(so that searchd can keep running even if we exit the shell).
```
$ sudo apt-get install tmux
$ cd $PROJECT/searchd
$ tmux new -d -s searchd_session './run/searchd.out -i ~/large-index'
```

At this point, you should be able to get search results back after
entering queries in demo page.

When you need to shutdown searchd, attach back this session:
```
$ tmux list-sessions
$ tmux attach -t searchd_session
```
and hit Ctrl-C.
