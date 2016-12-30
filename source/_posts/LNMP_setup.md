title: 配置 LNMP
date: 2016-4-3 08:55:29
tags: [PHP,Linux,Nginx,MySQL]
categories: 工具
toc: true
---
添加仓库并更新
```
sudo add-apt-respository ppa:nginx/stable
sudo add-apt-repository ppa:ondrej/php
sudo apt-get update
```

安装 php7 和 nginx
```
# 这里把 php7 和它的扩展一并安装了吧
sudo apt-get install php7.0 php7.0-*
sudo apt-get install nginx
```

配置账号
```
sudo useradd nginx
```

```
sudo vim /etc/nginx/nginx.conf
```
把 user 那行改成我们刚刚设置的 nginx
```
user nginx;
```


配置默认虚拟主机文件
```
sudo vim /etc/nginx/sites-enabled/default
```
主要修改这个部分
```
server {
	listen 80 default_server;
	listen [::]:80 default_server;
	# 这里把地址改成你的 web 文件夹地址
	root /path/to/web;

	# 这里改成 index.php
	index index.php;

	server_name _;

    # 这里实现伪静态
	location / {
		# First attempt to serve request as file, then
		# as directory, then fall back to displaying a 404.
		try_files $uri $uri/ /index.php?$args;
	}
	# 这里是关键
    location ~ \.php$ {
        try_files $uri =404;
        fastcgi_pass              127.0.0.1:9000;
        fastcgi_index             index.php;
        fastcgi_param             SCRIPT_FILENAME  $document_root$fastcgi_script_name;
        include                   fastcgi_params;
    }
}
```
修改 php-fpm 的配置
```
sudo vim /etc/php/7.0/fpm/pool.d/www.conf
```
主要修改这几个地方
```
user = nginx
group = nginx
listen.owner = nginx
listen.group = nginx
listen = 127.0.0.1:9000
```
到这里环境配置就基本完成了，接下来还有 MySQL 和 Composer 的配置。

