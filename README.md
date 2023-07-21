# Jython 2.1 backporting

[![CPython tests](https://github.com/LukeSavefrogs/jython21-backport/actions/workflows/run-python-tests.yml/badge.svg)](https://github.com/LukeSavefrogs/jython21-backport/actions/workflows/run-python-tests.yml)
[![Jython tests](https://github.com/LukeSavefrogs/jython21-backport/actions/workflows/run-jython-tests.yml/badge.svg)](https://github.com/LukeSavefrogs/jython21-backport/actions/workflows/run-jython-tests.yml)

Collection of features present in **newer Python** versions (`v2.x`, `v3.x`) backported to **legacy Python versions** (tested down to `v2.1`).

Supported Python implementation:

- [**CPython**](https://www.python.org/)
- [**Jython**](https://www.jython.org/)

## Features

This package provides backporting for the following features:

- [**`pathlib.Path()`**](src/polyfills/pathlib/) (`Python>=3.4`)
- [**`bool`**](src/polyfills/stdlib/future_types/bool.py) (`Python>=2.3`)
- [**`dict`**](src/polyfills/stdlib/future_types/dict.py)
- [**`sorted()`**](src/polyfills/stdlib/) (`Python>=2.4`)
- [**`collections.OrderedDict()`**](src/polyfills/collections/) (`Python>=2.7`)
- [**`json`**](src/polyfills/json/) module (`Python>=2.6`)

## Tests

After performing a change to a module it's best practice to **always run tests** and update those failing (or add some if it's a new feature).

### All repository

To run all the tests in this repository use the following command:

```shell
poetry run python -m unittest discover ./src/
```

You can test single files using the following commands:

### Single module

#### Locally

When developing using `poetry` use the following command:

```shell
poetry run python /path/to/module.py
```

For example:

```shell
(polyfills-py3.9) → ~\polyfills › poetry run python .\src\polyfills\pathlib\__init__.py
..........
----------------------------------------------------------------------
Ran 10 tests in 0.004s

OK
```

#### Remotely

To run tests on a host running the Websphere Application Server Jython console (`wsadmin.sh`) run the following command:

```shell
/path/to/profile/bin/wsadmin.sh -lang jython -f /path/to/module.py
```

For example:

```shell
username@hostname ~ $ /opt/Websphere/MyCell/profiles/dmgr/bin/wsadmin.sh -lang jython -f /src/polyfills/pathlib/__init__.py
WASX7209I: Connected to process "dmgr" on node MyNode using SOAP connector;  The type of process is: DeploymentManager
..........
----------------------------------------------------------------------
Ran 10 tests in 0.068s

OK
```
