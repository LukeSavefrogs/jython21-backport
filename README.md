# Jython 2.1 backporting

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

To run tests use the following command:

```shell
poetry run python -m unittest discover ./src/
```
