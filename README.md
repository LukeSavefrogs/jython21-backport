# Jython 2.1 backporting

[![CPython tests](https://github.com/LukeSavefrogs/jython21-backport/actions/workflows/run-python-tests-lin.yml/badge.svg)](https://github.com/LukeSavefrogs/jython21-backport/actions/workflows/run-python-tests-lin.yml)
[![CPython tests](https://github.com/LukeSavefrogs/jython21-backport/actions/workflows/run-python-tests-mac.yml/badge.svg)](https://github.com/LukeSavefrogs/jython21-backport/actions/workflows/run-python-tests-mac.yml)
[![CPython tests](https://github.com/LukeSavefrogs/jython21-backport/actions/workflows/run-python-tests-win.yml/badge.svg)](https://github.com/LukeSavefrogs/jython21-backport/actions/workflows/run-python-tests-win.yml)

[![Jython tests](https://github.com/LukeSavefrogs/jython21-backport/actions/workflows/run-jython-tests-lin.yml/badge.svg)](https://github.com/LukeSavefrogs/jython21-backport/actions/workflows/run-jython-tests-lin.yml)
[![Jython tests](https://github.com/LukeSavefrogs/jython21-backport/actions/workflows/run-jython-tests-mac.yml/badge.svg)](https://github.com/LukeSavefrogs/jython21-backport/actions/workflows/run-jython-tests-mac.yml)
[![Jython tests](https://github.com/LukeSavefrogs/jython21-backport/actions/workflows/run-jython-tests-win.yml/badge.svg)](https://github.com/LukeSavefrogs/jython21-backport/actions/workflows/run-jython-tests-win.yml)

Collection of features present in **newer Python** versions (`v2.x`, `v3.x`) backported to **legacy Python versions** (tested down to `v2.1`).

Supported Python implementation:

- [**CPython**](https://www.python.org/)
- [**Jython**](https://www.jython.org/)

## Features

This package provides backporting for the following features:

- [**`pathlib.Path()`**](src/polyfills/pathlib/) class (`Python>=3.4`)
- [**`bool()`**](src/polyfills/stdlib/future_types/) class (`Python>=2.3`) as well as `True` and `False` ([`Python>=2.3`](https://giedrius.blog/2018/01/04/what-is-actually-true-and-false-in-python/))
- [**`dict()`**](src/polyfills/stdlib/future_types/) class
- [**`sorted()`**](src/polyfills/stdlib/) function (`Python>=2.4`)
- [**`sum()`**](src/polyfills/stdlib/) function (`Python>=2.3`)
- [**`collections.OrderedDict()`**](src/polyfills/collections/) (`Python>=2.7`)
- [**`json`**](src/polyfills/json/) module (`Python>=2.6`)
- [**`logging`**](src/polyfills/logging/) module (`Python>=2.3`)
- [**`itertools`**](src/polyfills/itertools/) module (`Python>=2.3`)
- [**`set()`**](src/polyfills/stdlib/sets.py) class (`sets` module `Python>=2.3`, standard library `Python>=2.4`)
- [**`print()`**](src/polyfills/stdlib/) function (keyword arguments such as `end` or `sep` were added in `Python 3.3`, see module docstring for more details)

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
