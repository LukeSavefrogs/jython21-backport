""" Polyfill for the print function. 

WARNING:
    The `print` statement is not a function in Python 2! 
    
    Since it is a keyword, it cannot be redefined there, so if you really 
    need all the features of the newer `print`, you can:

    - Import the whole module:
    ```python
    import polyfills.stdlib.print as print

    print.print("Hello world!", {"a": 1, "b": 2}, [1, 2, 3], sep=" | ")
    ```
    - Import the function from the module and rename it to something else:
    ```python
    from polyfills.stdlib.print import print as prints

    prints("Hello world!", {"a": 1, "b": 2}, [1, 2, 3], sep=" | ")
    ```
"""
import sys as _sys

def print(*args, **kwargs):
    """ Print the given objects to the given file, separated by sep and followed by end.
    
    Args:
        *args: Objects to the printed
        sep (str, optional): Separator between objects. Defaults to " ".
        end (str, optional): End of the print. Defaults to "\n".
        file (file, optional): File to write the output. Defaults to None.
    """
    sep = kwargs.get("sep", " ")
    end = kwargs.get("end", "\n")
    file = kwargs.get("file", None)
    if file is None:
        file = _sys.stdout

    file.write(sep.join([str(arg) for arg in args]) + end)