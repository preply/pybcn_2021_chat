# Chat application project for PyBCN 2021 workshop

Proof of concept application for playing with Python and other technologies (like Websockets)

## Requirements
- [Docker](https://docs.docker.com/install/)
- [Docker-compose](https://docs.docker.com/compose/install/)


## Usage

```bash
make <command>
```

List of available commands:

- `run`  build application containers and run with dev server (runs all new db migrations)
- `build` build application containers
- `admin` add superuser
- `stop` stop application and all its containers
- `db` initialize application database
- `migrate` generate database migration file
- `upgrade` apply latest database migration files
- `merge-heads` generate database migration file for heads merging
- `bash` open bash shell inside app container
- `dbshell` run pimped out database shell inside db container
- `redis-cli` run redis shell in redis container
- `test` run all tests
- `test file=path/to/tests.py::some_test` run separate dir/module/test

## Run server

```bash
make run
```

> May ask for superuser rights (for Docker)
## Swagger
Swagger is available after running server ([http://localhost:5000/docs/](http://localhost:5000/docs/))
