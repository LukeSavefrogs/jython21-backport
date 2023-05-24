""" This package provides polyfills for features that will be added in newer Python versions.

The polyfills are organized in subpackages, each one containing the polyfills for a specific
Python module. For example, the `polyfills.stdlib.pathlib` package contains the
polyfills for the `pathlib` module.
"""
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
        import java  # type: ignore
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

def get_jython_type(obj):
    """Return a string representation of the type of the provided object.

    Works both in regular Python and Jython.

    WARNING: because of Jython's limitations it CANNOT detect a boolean type!

    http://graphexploration.cond.org/javadoc/org/python/core/package-summary.html
    ['Py', 'PyArray', 'PyBeanEvent', 'PyBeanEventProperty', 'PyBeanProperty',
    'PyBuiltinFunctionSet', 'PyCell', 'PyClass', 'PyCode', 'PyComplex',
    'PyCompoundCallable', 'PyDictionary', 'PyEllipsis', 'PyException', 'PyFile',
    'PyFinalizableInstance', 'PyFloat', 'PyFrame', 'PyFunction',
    'PyFunctionTable', 'PyIgnoreMethodTag', 'PyInstance', 'PyInteger',
    'PyJavaClass', 'PyJavaInnerClass', 'PyJavaInstance', 'PyJavaPackage',
    'PyList', 'PyLong', 'PyMetaClass', 'PyMethod', 'PyModule', 'PyNone',
    'PyNotImplemented', 'PyObject', 'PyProxy', 'PyReflectedConstructor',
    'PyReflectedField', 'PyReflectedFunction', 'PyRunnable', 'PySequence',
    'PySingleton', 'PySlice', 'PyString', 'PyStringMap', 'PySyntaxError',
    'PySystemState', 'PyTableCode', 'PyTraceback', 'PyTuple', 'PyXRange']

    Args:
        obj (any): The object we need to know the type of.

    Returns:
        type(str): The type of the provided object.
    """
    try:                                # Try checking the string representation
        type_name = type(obj).__name__
        if type_name in ["list", "org.python.core.PyList"]:
            return "list"
        elif type_name in ["tuple", "org.python.core.PyTuple"]:
            return "tuple"
        elif type_name in ["dict", "org.python.core.PyDictionary"]:
            return "dict"
        elif type_name in ["str", "org.python.core.PyString"]:
            return "str"
        elif type_name in ["int", "org.python.core.PyInteger"]:
            return "int"
        elif type_name in ["float", "org.python.core.PyFloat"]:
            return "float"
        elif type_name in ["function", "org.python.core.PyFunction"]:
            return "function"
        elif type_name in ["class", "org.python.core.PyClass"]:
            return "class"
        elif type_name in ["NoneType", "org.python.core.PyNone"]:
            return "NoneType"
        else:
            return "unknown"
    except:                             # Fallback to duck typing
        available_methods = dir(obj)
        if ("append" in available_methods) and ("extend" in available_methods) and ("pop" in available_methods):
            return "list"
        elif ("count" in available_methods) and ("index" in available_methods) and ("append" not in available_methods):
            return "tuple"
        elif ("clear" in available_methods) and ("items" in available_methods) and ("keys" in available_methods):
            return "dict"
        elif len([method for method in available_methods if method.startswith("_")]) == len(available_methods):
            return "NoneType"
        else:
            raise Exception("Couldn't find more info about the type of '%s' using duck typing" % str(obj))
