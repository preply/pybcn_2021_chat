# pybcn_2021_chat
Chat application project for PyBCN 2021 workshop

## Requirements
- [Docker](https://docs.docker.com/install/)
- [Docker-compose](https://docs.docker.com/compose/install/)

## Swagger
Swagger is available after running server ([http://localhost:5000/docs/](http://localhost:5000/docs/))

```bash
make run
```

## Usage

```bash
make <command>
```

> May ask superuser rights (for docker)

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

# Module directory structure:
```tree
my_microservice
├── app
│   └── some_module
│       ├── models.py <---- data models
│       ├── views.py  <---- endpoints
│       ├── crud.py   <---- db wrapper
│       ├── constants.py
│       ├── utils.py
│       └── shemas.py  <---- data schemas
└── tests
    └── mimics app
```
