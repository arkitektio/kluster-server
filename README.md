# Kluster-Server


[![codecov](https://codecov.io/gh/arkitektio/kluster-server/branch/main/graph/badge.svg?token=UGXEA2THBV)](https://codecov.io/gh/arkitektio/kluster-server)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/arkitektio/kluster-server/)
![Maintainer](https://img.shields.io/badge/maintainer-jhnnsrs-blue)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/jhnnsrs/arkitektio/kluster-server)

## Develompent

Kluster is a GraphQL API that allows you to to interact and create a variety of Clusters, and interact with
them in a variety of ways. Currently we support the following:

-   Dask Gateway Clusters
  
    These are clusters that are managed by a Dask Gateway server. They can be created and destroyed at will,
    and are designed to be ephemeral. They are designed to be used for batch processing, and are not designed
    to be used for long running jobs. Please use the "jhnnsrs/kluster-gateway" docker image to run a Dask Gateway
    server, that allows pass through authentication.


### Design

We use the Strawberry Extensions system to pass a `single` user authenticated Dask Gateway session through
the GraphQL resolvers. This should reduce the number of times we need to connect to the dask gateway server
and create new sessions.


> [!NOTE]  
> What you are currently looking is a service that is not yet part of a standard Arkitekt Deployment. It is currently under development and not ready for production. .


Check out the [documentation](https://arkitekt.live/docs/services/next/kluster) for more information.


## Roadmap

This is the current roadmap for the merging of the new version of Lok into the main repository:

- [x] CI/CD Pipeline
- [ ] Documentation
- [ ] Better Testing
