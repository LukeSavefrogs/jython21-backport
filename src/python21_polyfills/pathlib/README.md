# `pathlib`

Backport of the `pathlib.Path` module.

## Usage

```python
from pathlib import Path

print(Path("~/.ssh/").expanduser().exists())
```
