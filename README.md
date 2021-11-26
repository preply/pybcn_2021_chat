# Chat application project for PyBCN 2021 workshop

Proof of concept application for playing with Python and other technologies (like Websockets), as part of the [PyBCN 2021](https://pybcn.org/events/pyday_bcn/pyday_bcn_2021/) event

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
- `test` run all tests
- `test file=path/to/tests.py::some_test` run separate dir/module/test

## Run server

```bash
make run
```

> May ask for superuser rights (for Docker)
## Swagger
Swagger is available after running server ([http://localhost:5000/docs/](http://localhost:5000/docs/))
