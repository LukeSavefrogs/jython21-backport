# python2-json

Basic implementation of a **JSON parser** written in pure Python and created as a **drop-in replacement** (_well, almost_) for the `json` module in environments using **very old Python versions** (`2.2` and lower).

Provides `loads`, `dumps` and their counterparts `load` and `dump`.

> **_Please note that speed is clearly not the focus here..._**

## Features

- **Same function names** and signature: `loads`, `dumps`, `load`, `dump`;
- Handles all **base JSON types**:
  - _Arrays_: `[]`
  - _Objects_: `{}`
  - _Strings_: `""`
  - _Numbers_: integers (`3`), floating point (`3.14`), exponential (`3.14e10`)
  - _Boolean_: `true` and `false`
  - _Null_: `null`
- Handles **nested data structures**, such as:

   ```json
   { "key": "value", "nested": [{"name": "first", "elems": [1, true,null]}] }
   ```

    If passed through the `loads(...)` method will return:

    ```python
    {'key': 'value', 'nested': [{'name': 'first', 'elems': [1, True, None]}]}
    ```

## Known limitations & gotchas

### Gotchas 👀

- `Infinity` and `NaN` currently do not follow strictly the `json` module rules (still no `allow_nan` parameter).
- If using this module on **Python 2.3 and lower** you _may need_ to pass `truthy_value` and `falsy_value`;

### Known bugs 🐛

These are some known bugs that will be fixed in the next releases:

- **Does not convert unicode strings** to the respective character and viceversa (e.g. `\u1eb7` is not converted to `ặ`).

    ```pycon
    >>> json.loads('"\\u1eb7 \\u00a3"')
    - ORIGINAL: 'ặ £'
    - THIS    : '\\u1eb7 \\u00a3'

    >>> json.dumps('ặ £')
    - ORIGINAL: '"\\u1eb7 \\u00a3"'
    - THIS    : '"ặ £"'
    ```

## Resources

- [JSON specification](https://www.json.org/json-en.html)

## Valid alternatives

These are some valid alternatives if this is not what you're looking for (_as it probably is and should be_), ordered by minimum supported version.

<table>
    <thead>
        <tr>
            <th>Library</th>
            <th>Description</th>
            <th>Built-in</th>
            <th>Supported Python versions</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>
                <code><a href="https://github.com/simplejson/simplejson/tree/python2.2">simplejson/python2.2</a></code>
            </td>
            <td>
                Branch of the <code>simplejson</code> library that mantains backwards compatibility with Python 2.2.
                Makes use of generator functions that were introduced in Python 2.2 (via <a href="https://peps.python.org/pep-0255/">PEP 255</a>).
            </td>
            <td>
                No
            </td>
            <td>
                <code>Python >= 2.2</code>
            </td>
        </tr>
        <tr>
            <td>
                <code><a href="https://github.com/dmeranda/demjson">demjson</a></code>
            </td>
            <td>
                Feature rich module that uses only built-in methods and allows to encode, decode and syntax-checking JSON data.
            </td>
            <td>
                No
            </td>
            <td>
                <a href="https://github.com/dmeranda/demjson/blob/5bc65974e7141746acc88c581f5d2dfb8ea14064/docs/INSTALL.txt#L8-L10"><code>Python >= 2.4</code></a>
            </td>
        </tr>
        <tr>
            <td>
                <code><a href="https://github.com/simplejson/simplejson">simplejson</a></code>
            </td>
            <td>
                Externally maintained development version of the built-in <code>json</code> library included with Python.
            </td>
            <td>
                No
            </td>
            <td>
                <a href="https://github.com/simplejson/simplejson/blob/9559fc756deaf20b6bae961b58c5289d8582c8b7/README.rst?plain=1#L4-L6"><code>Python >= 2.5</code></a>
            </td>
        </tr>
        <tr>
            <td>
                <code><a href="https://docs.python.org/3/library/json.html">json</a></code>
            </td>
            <td>
                <b>Built-in</b> library included with Python.
            </td>
            <td>
                <i>Yes</i>
            </td>
            <td>
                <code>Python >= 2.6</code>
            </td>
        </tr>
        <tr>
            <td>
                <code><a href="https://github.com/ijl/orjson">orjson</a></code>
            </td>
            <td>
                Fast JSON library written in Rust that serializes various data structures, such as <code>dataclass</code>, <code>datetime</code>/<code>date</code>/<code>time</code> and <code>numpy.ndarray</code> instances.
            </td>
            <td>
                No
            </td>
            <td>
                <a href="https://github.com/ijl/orjson/blob/a60506c77e7051774dddd86bb8c12ec4a79223d5/README.md?plain=1#L35"><code>CPython >= 3.7</code></a>
            </td>
        </tr>
        <tr>
            <td>
                <code><a href="https://github.com/ultrajson/ultrajson">ujson</a></code>
            </td>
            <td>
                Ultra fast JSON encoder and decoder written in pure C.
            </td>
            <td>
                No
            </td>
            <td>
                <a href="https://github.com/ultrajson/ultrajson/blob/6035e09077e6bd3e8e3e91162bb1232507967735/README.md?plain=1#L11-L12"><code>Python >= 3.7</code></a>
            </td>
        </tr>
        <tr>
            <td>
                <code><a href="https://github.com/python-rapidjson/python-rapidjson">python-rapidjson</a></code>
            </td>
            <td>
                Python 3 wrapper around <code>RapidJSON</code>, an extremely fast C++ JSON parser and serialization library
            </td>
            <td>
                No
            </td>
            <td>
                <code>Python >= 3.x</code><br><i>(unknown minor)</i>
            </td>
        </tr>
    </tbody>
</table>

## Development

1. **Clone** the repository
2. **Install** with `poetry install --with dev`

### Tests

**Tests ensure** that changes to the codebase **do not break existing features** and that anything **works as expected**.

To launch the tests run the following command:

```shell
poetry run poe test
```

Please make sure to...

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
