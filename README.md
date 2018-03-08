# Django Twitter Notifier

## Setup mysql

- install mysql

``` shell
$ sudo apt-get update
$ sudo apt-get install mysql-server
$ sudo apt-get install libmysqlclient-dev
```

- add user to mysql

``` shell
$ sudo mysql
```

``` sql
> USE mysql;
> CREATE USER user1@localhost IDENTIFIED BY 'your password';
> SELECT user, host from user; # check
```

- create databases

``` sql
> CREATE DATABASE twitternotifier;
```

- create tables

``` sql
> USE twitternotifier;
CREATE TABLE `twitter_favorites` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `tweet_id` varchar(255) UNIQUE,
  `tweet` varchar(300) NOT NULL,
  `user_id` varchar(255) NOT NULL,
  `user_name` varchar(255) NOT NULL,
  `user_screen_name` varchar(255) NOT NULL,
  `created_at` datetime NOT NULL,
  `update_at` datetime NOT NULL,
  `favorite_count` integer NOT NULL,
  `retweet_count` integer NOT NULL,
  `original_url` varchar(255) NOT NULL,
  PRIMARY KEY (`id`) 
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='twitter favorite table';
  
CREATE TABLE `twitter_retweets` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `tweet_id` varchar(255) UNIQUE,
  `tweet` varchar(300) NOT NULL,
  `user_id` varchar(255) NOT NULL,
  `user_name` varchar(255) NOT NULL,
  `user_screen_name` varchar(255) NOT NULL,
  `created_at` datetime NOT NULL,
  `update_at` datetime NOT NULL,
  `favorite_count` integer NOT NULL,
  `retweet_count` integer NOT NULL,
  `original_url` varchar(255) NOT NULL,
  PRIMARY KEY (`id`) 
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='twitter retweet table';
```

- grant users

``` sql
> GRANT ALL PRIVILEGES ON twitternotifier.* TO 'user1'@'localhost' IDENTIFIED BY 'your password';
```

## Install requirements

``` shell
$ pip install -r requirements.txt
```

## Copy some setting files

``` shell
$ cp twitternotifier/static_settings.py.example twitternotifier/static_settings.py
$ cp twitternotifier/database.py.example twitternotifier/database.py
```

## Setup django-jet dashboard

``` shell
$ python manage.py migrate
$ python manage.py migrate jet
$ python manage.py migrate dashboard
```

## Setup some apps

``` shell
$ python manage.py makemigrations favorites
$ python manage.py makemigrations retweets
```

## Create user

``` shell
$ python manage.py createsuperuser
Username (leave blank to use 'xxx'):
Email address: (Enter)
Password: (Input password)
Password (again): (Input password again)
```

## Start server

``` shell
$ python manage.py runserver 0:8000
```

## Get favorites and retweets

``` shell
$ python manage.py get_tweets
```

## Notify to slack

``` shell
$ python manage.py notify_slack
```
