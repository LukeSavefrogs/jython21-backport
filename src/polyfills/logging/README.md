# `logging`

This module provides a polyfill for the `logging` module (_introduced in Python 2.3_).

## Features

- Initialization possible via **`getLogger`** function (_as in the original module_) or `Logger` class
- Logs printed only if **level is enabled** (_e.g. `logger.debug(...)` will not print anything if level is set to `INFO`_)
- Logger can have custom names (_default is `root`_)

## Usage

### Initialization via `basicConfig(...)`

This method will allow you to initialize the root logger with a single call.
To use the root logger just call the log methods on the `logging` module itself:

```python
import polyfills.logging as logging

# NOTE: All parameters are optional
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

logging.debug("This will not be printed")
logging.info("This will be printed")
```

### Initialization via `getLogger(...)`

This method will allow you to initialize a custom logger. To use the custom logger just call the log methods on the newly created logger:

```python
import polyfills.logging as logging

logger = logging.getLogger("my_logger")
logger.setLevel(logging.INFO)        # Set level to 'INFO' (default is 'NOTSET')

logger.debug("This will not be printed")
logger.info("This will be printed")
```

> **WARNING:**
>
> At the moment, since the **`Formatter`** class is **still not implemented** if you use the `getLogger` method, you will not be able to change the format of the logs.
>
> Currently, the only supported way to do this is to use the `basicConfig` function.
>
> A workaround would be to use the internal properties `logger._format` and `logger._time_format` to change the format of the logs:
>
> ```python
> logger = logging.getLogger("my_logger")
> logger._format = "[%(asctime)s] %(levelname)s - %(name)s - %(message)s"
> ```
>
> Keep in mind that **things might change in the future**, so use this workaround at your own risk!

## ⚠️ Known limitations & gotchas

- To keep things simple, this module is [**NOT thread-safe**](https://superfastpython.com/thread-safe-logging-in-python/) (_this will make the difference ONLY if you need to write logs from multiple threads_).
- The **`basicConfig`** function is implemented but some of its features are missing:
  - `filename`/`filemode`/`encoding`/`errors`: **Files are not supported** (_logs are always printed to `stdout`_)
  - `style`: Currently only the **default style is supported** (_same as `style='%'`_)
  - `stream`: **Streams are not supported**
  - `handlers`: Custom **handlers are not supported**
  - `force`: Currently every call to the `basicConfig` function **overwrites the previous configuration** (same as `force=True`)
- The **`Logger`** object...
  - **cannot have custom `filters` or `handlers`** (no `addFilter` or `addHandler` methods)
  - has a **slightly different signature**, with `fmt` and `datefmt` being set via constructor instead of a `Formatter` class
