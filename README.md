# pacer-demo

## System Requirements

1. Python >=3.8.13
2. PostgreSQL >=9.4
3. Django >=4.1.2

### Scripts

- Run this command to initialize directories and load permissions into database:
```sh
$ python manage.py initialize
```

- Run this command as a shortcut for makemigrations and migrate:
```sh
$ python manage.py migration_call
```
or 
```sh
$ python manage.py migration_call --app={app_name}
```
**Notes**: Replace `app_name` tag with a app name