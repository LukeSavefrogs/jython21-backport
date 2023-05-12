![Python version](https://img.shields.io/static/v1?label=python&message=>%3D2.1&color=informational&style=for-the-badge)
[![License](https://img.shields.io/github/license/LukeSavefrogs/python21-OrderedDict?color=green&style=for-the-badge)](https://github.com/LukeSavefrogs/python21-OrderedDict/blob/master/LICENSE)

[![Run tests](https://github.com/LukeSavefrogs/python21-OrderedDict/actions/workflows/run-tests.yml/badge.svg)](https://github.com/LukeSavefrogs/python21-OrderedDict/actions/workflows/run-tests.yml)
[![Open issues](https://img.shields.io/github/issues-raw/LukeSavefrogs/python21-OrderedDict?color=yellow)](https://github.com/LukeSavefrogs/python21-OrderedDict/issues?q=is%3Aissue+is%3Aopen+)

# OrderedDictionary

Backporting of the `OrderedDict` class from the `collection` package that can be used in **legacy Python 2** scripts (_tested on Python 2.1_).

## What is an `OrderedDict`?

Quoting from [RealPython's tutorial](https://realpython.com/python-ordereddict/):
> Python’s `OrderedDict` is a `dict` subclass that **preserves the order** in which key-value pairs, commonly known as items, are **inserted into the dictionary**.
>
> - When you iterate over an OrderedDict object, items are traversed in the original order.
> - If you update the value of an existing key, then the order remains unchanged.
> - If you remove an item and reinsert it, then the item is added at the end of the dictionary.

## Roadmap

Since `OrderedDict` is a `dict` subclass. we need to implement all dictionary methods:

- [X] `.clear()`
- [X] `.copy()`
- [ ] `.get(key, default)`
- [ ] `.update(object)`
- [ ] `.setdefault(key, default)`
- [ ] `.pop(key, default)`
- [ ] `.popitem()`
- [ ] `.move_to_end(key, last)`
- [ ] `.fromkeys(keylist, value)`

## Special thanks

The [**original version**](https://github.com/amina196/OrderedDictionary) was uploaded by [@Amina Bouabdallah](https://github.com/amina196) on **May 26, 2012**
(_11 years ago at the moment of writing_).

I just blew the dust off the repo, adjusted the code to work on Jython 2.1 and added some features.

## Development

1. **Clone** the repository.
1. **Install** all the **development dependencies** with:

    ```shell
    poetry install --with dev
    ```

1. Experiment
1. Create and **run tests**

### Tests

**Tests ensure** that changes to the codebase **do not break existing features** and that anything **works as expected**.

Please be sure to...

- ... keep existing tests up-to-date with the latest **changes**;
- ... write relative tests when adding **new features**.

#### Tests code style

When writing tests please keep the in mind that:

- test files MUST be written for `unittest`;
- _test cases_ names MUST be a descriptive name written in PascalCase and end with `TestCase` (e.g. `class MyTestCase(unittest.TestCase):`);
- _test_ names MUST be a descriptive name written in snake_case (_all lowercase, with words separated with an underscore_) and start with `test_` (e.g. `def test_feature(self):`);
- MAY use the [`setUp()`](https://docs.python.org/3/library/unittest.html#unittest.TestCase.setUp) and [`teardown()`](https://docs.python.org/3/library/unittest.html#unittest.TestCase.tearDown) methods to define instructions that will be executed before and after each test method;
- each test MUST contain at least one `self.assert*` method call (we don't want empty no-op tests);

The following is an example of agood test from the official Python documentation:

```python
import unittest

class WidgetTestCase(unittest.TestCase):
    def setUp(self):
        self.widget = Widget('The widget')

    def tearDown(self):
        self.widget.dispose()

    def test_default_widget_size(self):
        self.assertEqual(
            self.widget.size(),
            (50,50),
            'incorrect default size'
        )

    def test_widget_resize(self):
        self.widget.resize(100,150)
        self.assertEqual(
            self.widget.size(),
            (100,150),
            'wrong size after resize'
        )
```
