# `pathlib`

Backport of the `pathlib` module for Jython 2.1.

Implemented mostly by using native `os.path` calls to mimic the behaviour of the `pathlib.Path` class.

## Features

- **Initialization** with string or parameters (`Path("/tmp/sub_dir")` or `Path("/tmp", "sub_dir")`)
- **Path concatenation** through the division operator (`Path("/tmp") / "sub_dir"`)
- Same output for both `str(...)` and `repr(...)`
- Subset of **methods** from the original `Path`:
  - `.absolute()`
  - `.resolve()`
  - `.expanduser()`
  - `.exists()`
  - `.unlink()`
  - `.read_bytes()` and `.read_text()`
  - `.write_bytes()` and `.write_text()`

## Usage

```python
from pathlib import Path

print(Path("~/.ssh/").expanduser().exists())
```
