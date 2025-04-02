# Authentication as a Service

The python project **Authentication as a Service** (short: _aaas_) is a production grade, drop in authentication module. Aaas provides a fully fledged role based authentication service using JWT through a secure application programming gateway (sapgw). With simplicity kept in mind, it acts like a general purpose authentification micro service. Aaas is part of the x-aas series where I design production grade services for repeating tasks.

## Features

- JWT with ES512 (needs to be generated in advance)
- User Registration with username, email, password
- User Login
- Administration options
  - User administration (CRUD Operations)
  - Role administration (CRUD Operations)
- Hashing with argon2id

## System design

Due to its central role, aaas was designed to be a _function-first_ service.
The platform is split in seven parts with each serving one special purpose.

**List of parts:**

- `core` - Essential System wide functions (e.g. configuration, security, certificates ...)
- `db` - sqlalchemy DB setup
- `crud` - CRUD operations for the DB tables
- `models` - table definitions using sqlalchemy
- `routes` - FastAPI Routes
- `schemas` - Response and DB schemas (pydantic)
- `services` - Business Logic of the services

All crud operations, routes, services and all core functions (except of the configuration) is tested using pytest.

## TO Do

- [ ]  Licence, Issue Tracker,...
- [ ] Documentation
- [ ] Initialise tests
- [ ] implement basic FastAPI structure
- [ ] Hashing bla
- [ ] JWT
