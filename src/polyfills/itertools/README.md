# `itertools`

Backport of the `itertools` module for Jython 2.1.

This module was first introduced into the Python standard library in version 2.3.

## Usage

```python
from polyfills import itertools

print(itertools.batched("Hello World", 3)) # Output: ['Hel', 'lo ', 'Wor', 'ld']
```
