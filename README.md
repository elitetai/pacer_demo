# pacer_demo

## System Requirements

1. Python>=3.8.13
2. PostgreSQL>=14.3

## Local Setup

1. Clone the repository:

    ```sh
    $ git clone https://github.com/elitetai/pacer_demo.git
    $ cd pacer_demo
    ```

1. Install the dependencies:

    ```sh
    $ pip install -r requirements.txt
    ```

1. You will need to create an `.env` file in the root folder of this project

1. Run the database migrations

    ```sh
    $ python manage.py migrate
    ```

1. collects static files into root folder of the project

    ```sh
    $ python manage.py collectstatic
    ```

1. Run this command to initialize directories and load permissions into database:

    ```sh
    $ python manage.py initialize
    ```

1. Run this command to start the server:

    ```sh
    $ python manage.py runserver
    ```

## Additional Scripts

- Run this command as a shortcut for makemigrations and migrate:

```sh
$ python manage.py migration_call
```
or 

**Notes**: Replace `app_name` tag with a app name
```sh
$ python manage.py migration_call --app={app_name}
```