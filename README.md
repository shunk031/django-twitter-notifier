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
> CREATE DATABASE twitterfavotites;
> CREATE DATABASE twitterretweets;
```

- create tables

``` sql
> USE twitterfavorites;
> CREATE TABLE 
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

## Copy some setting files

``` shell
$ cp twitternotifier/static_settings.py.example twitternotifier/static_settings.py
$ cp twitternotifier/database.py.example twitternotifier/database.py
```

## Start server

``` shell
$ python manage.py runserver 0:8000
```
