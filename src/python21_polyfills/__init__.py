import sys
import os


def is_jython():
    """Detect if the Python implementation is Jython.

    Returns:
        bool: Wether the current Python implementation is Jython
    """
    _false = 1 == 0
    _true = 1 == 1

    # Method 1: Check if the `java` package is installed
    try:
        import java  # pyright: ignore[reportMissingImports]
    except ImportError:
        return _false

    # Method 2: Check if the runtime is "Java(TM) SE Runtime Environment"
    runtime = str(java.lang.System.getProperty("java.runtime.name"))

    # Method 3: Check if the platform is "java{JDK_version}" (ex. "java1.8.0_351")
    platform = str(sys.platform).lower()

    # Method 4: Check if the os name is set to "java"
    operative_system = os.name.lower()

    return (
        runtime == "Java(TM) SE Runtime Environment"
        and platform.startswith("java")
        and operative_system == "java"
    )
