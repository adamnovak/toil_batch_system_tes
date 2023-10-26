# Toil TES Batch System

This package contains the TES batch system implementation that was removed from
Toil after version 5.12. It allows the [Toil workflow engine](https://toil.readthedocs.io/en/latest/)
to run workflows on servers that implement [the GA4GH Task Execution Schemas API](https://github.com/ga4gh/task-execution-schemas).

If you intall it, newer versions of Toil will pick up that it is installed, import it, and allow you to use it with `--batchSystem tes`.

## Installation

1. Create and enter a Python environment with Toil >5.12 installed. Note that as of this writing no release newer than 5.12 exists; you may need to install Toil from source.

2. Clone this repository.

3. Enter the directory you cloned the repository to.

4. Run `pip install .`.

## Usage

To use the TES batch system, run a workflow with `--batchSystem tes`, and
configure a username and passowrd or a bearer token for authentication (see
below). You might also need to use the AWS job store, or another job store
accessible over the network.

This plugin adds the following options to Toil:

```
  --tesEndpoint TES_ENDPOINT
                        The http(s) URL of the TES server.
                        (default: http://<leader IP>:8000)
  --tesUser TES_USER    User name to use for basic authentication to TES server.
  --tesPassword TES_PASSWORD
                        Password to use for basic authentication to TES server.
  --tesBearerToken TES_BEARER_TOKEN
                        Bearer token to use for authentication to TES server.
```

They can be configured using the following environment variables:

```
+----------------------------------+----------------------------------------------------+
| TOIL_TES_ENDPOINT                | URL to the TES server to run against when using    |
|                                  | the ``tes`` batch system.                          |
+----------------------------------+----------------------------------------------------+
| TOIL_TES_USER                    | Username to use with HTTP Basic Authentication to  |
|                                  | log into the TES server.                           |
+----------------------------------+----------------------------------------------------+
| TOIL_TES_PASSWORD                | Password to use with HTTP Basic Authentication to  |
|                                  | log into the TES server.                           |
+----------------------------------+----------------------------------------------------+
| TOIL_TES_BEARER_TOKEN            | Token to use to authenticate to the TES server.    |
+----------------------------------+----------------------------------------------------+
```
