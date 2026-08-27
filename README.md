# Toil TES Batch System

Find us on [PyPI](https://pypi.org/project/toil-batch-system-tes)!

This package contains the TES batch system implementation that was removed from
Toil after version 5.12. It allows the [Toil workflow engine](https://toil.readthedocs.io/en/latest/)
to run workflows on servers that implement [the GA4GH Task Execution Schemas API](https://github.com/ga4gh/task-execution-schemas).

If you intall it, newer versions of Toil will pick up that it is installed, import it, and allow you to use it with `--batchSystem tes`.

## Installation

1. Create and enter a Python environment with Toil >=6.2 installed.

2. Clone this repository.

3. Enter the directory you cloned the repository to.

4. Run `pip install .`.

## Usage

To use the TES batch system, run a workflow with `--batchSystem tes`, and
configure a username and passowrd or a bearer token for authentication (see
below). You might also need to use the AWS job store, or another job store
accessible over the network.

This plugin targets TES 1.1 servers and depends on `py-tes>=1.1`.

## Kubernetes shared `file:/` jobstore caveat

When using a shared filesystem job store (for example `--jobStore file:/shared/toil-jobstore`) on Kubernetes, jobs can fail even when TES endpoint configuration is correct.

The most common cause is UID/GID mismatch between the process writing the job store (often the Toil driver) and the process reading/writing it in TES task pods. This can present as runtime failures with missing executor logs, permission denied errors, or cleanup failures.

Potential mitigations:

- Run driver and task pods with compatible identity (`runAsUser`/`runAsGroup`).
- Use `fsGroup` so shared volume contents are group-accessible.
- If needed, pre-create/chown the shared directory to the runtime UID/GID before invoking Toil.
- For smoke tests, consider `--clean never` and perform cleanup separately with a compatible identity.
- For production, prefer network/object-backed job stores when feasible to avoid shared filesystem ownership coupling.

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
| TOIL_TES_SKIP_STORAGE_CHECK      | Set to `1` to skip server storage mountability     |
|                                  | pre-checks. Use with caution: invalid mounts may   |
|                                  | fail later at runtime instead of at startup.       |
+----------------------------------+----------------------------------------------------+
```

## Developing the Plugin

When working on this plugin, make sure to update the range of required Toil version when the Toil batch system API changes.

To publish to PyPI, make sure you have an account-scope or project-scope authentication token configured. Then run:
```
python3.9 -m virtualenv venv
. venv/bin/activate
pip install setuptools wheel build twine
rm -Rf dist/
python -m build
ls dist/
twine upload dist/*
```
