""" Not all `os.path` methods are available for Jython.

```
wsadmin>dir(os.path)
['File', 'System', '__doc__', '__file__', '__name__', '_tostr', 'abspath', 'basename', 'commonprefix', 'dirname', 'exists', 'expanduser', 'expandvars', 'getatime', 'gethome', 'getmtime', 'getsize', 'getuser', 'isabs', 'isdir', 'isfile', 'islink', 'ismount', 'java', 'join', 'normcase', 'normpath', 'os', 'samefile', 'split', 'splitdrive', 'splitext', 'walk']
```
"""
import os as _os
import unittest

try:
    from pathlib import Path as _Path
except ImportError:
    pathlib_available = 0
else: 
    pathlib_available = 1


__all__ = ["Path"]

class Path:
    _path = ""
    _class_type = "" # valid types: Posix | Windows

    def __init__(self, *args, **kwargs):
        exec("import os as _os")
        if _os.name == 'nt':
            self._class_type = "Windows"
            self._path = _os.path.join(*args).replace("/", "\\")
        else:
            self._class_type = "Posix"
            self._path = _os.path.join(*args)
        
        if self._path.replace("\\", "/").startswith("./"):
            self._path = self._path[2:]
        
    def __str__(self):
        return str(self._path)
    
    def __repr__(self):
        return "%s('%s')" % (self._class_type + "Path", str(self._path).replace("\\", "/"))
    
    def __div__(self, other):
        if str(self) == ".":
            return Path(str(other))
        
        return Path(str(self), str(other))
    
    def __truediv__(self, other):
        if str(self) == ".":
            return Path(str(other))
        
        return Path(str(self), str(other))
    
    def __rdiv__(self, other):
        if str(other) == ".":
            return Path(str(self))
        
        return Path(str(other), str(self))
    
    def __rtruediv__(self, other):
        if str(other) == ".":
            return Path(str(self))
        
        return Path(str(other), str(self))
    
    def absolute(self):
        """Return an absolute version of this path.  This function works
        even if the path doesn't point to anything.

        No normalization is done, i.e. all '.' and '..' will be kept along.
        Use resolve() to get the canonical path to a file.
        """
        parts = self._path.replace("\\", "/").split("/")
        if parts[-1].strip() == "":
            parts.pop()

        if parts[0] == ".":
            self._path = _os.path.join(_os.path.abspath("."), *parts[1:])
        
        return Path(self._path)
    
    # WORKS (needs testing for symlinks)
    def resolve(self):
        """ Make the path absolute, resolving all symlinks on the way and also
        normalizing it (for example turning slashes into backslashes under
        Windows). 
        """
        return Path(_os.path.abspath(_os.path.normpath(self._path)))
    
    # WORKS
    def expanduser(self):
        return Path(_os.path.expanduser(self._path))

    # WORKS
    def exists(self):
        """ Whether this path exists. """
        return _os.path.exists(str(Path(self._path).resolve()))
    
    def unlink(self):
        _os.remove(str(Path(self._path).resolve()))

    def read_bytes(self):
        """
        Open the file in bytes mode, read it, and close the file.
        """
        return self._safe_read(self._path, mode='rb')
        
    def read_text(self, mode="r"):
        """
        Open the file in text mode, read it, and close the file.
        """
        return self._safe_read(self._path, mode='r')


    def write_bytes(self, data):
        """
        Open the file in bytes mode, write to it, and close the file.
        """
        return self._safe_write(self._path, data, mode="wb")

    def write_text(self, data):
        """
        Open the file in text mode, write to it, and close the file.
        """
        return self._safe_write(self._path, data, mode="w")


    def _safe_read(self, filename, mode="r"):
        """Wrapper around the classic `open` function which makes sure to always
        close the file even after an exception.

        Raises:
            Exception: The specified file was not found.
            IOError: An error occurred while trying to read the file.

        Returns:
            data (str): The data saved in the file.
        """
        try:
            try:
                file = open(filename, mode)
                return str(file.read())
            except Exception:
                raise
        finally:  # see https://stackoverflow.com/a/10946408/8965861
            try:
                file.close()  # type: ignore
            except:
                pass

    def _safe_write(self, filename, data, mode="w"):
        """Wrapper around the classic `open` function which makes sure to always
        close the file even after an exception.

        Args:
            filename (str): Absolute or relative path to the file.
            data (Any): The data that needs to be written. The function is also responsible for its string conversion.

        Raises:
            IOError: An error occurred while trying to write the file.
        """
        try:
            try:
                file = open(filename, mode)
                file.write(str(data))
            except Exception:
                raise 
        finally:
            try:
                file.close()  # type: ignore
            except:
                pass


class PathTestCase(unittest.TestCase):
    def test_creation(self):
        self.assertEqual(str(Path("/", "tmp", "", "test.py")), "%stmp%stest.py" % (_os.sep, _os.sep))
        self.assertEqual(str(Path("/tmp/test.py")), "%stmp%stest.py" % (_os.sep, _os.sep))
        
    def test_dots(self):
        self.assertEqual(str(Path(".")), ".")
        self.assertEqual(str(Path("./..")), "..")
        self.assertEqual(str(Path("../..")), "..%s.." % (_os.sep))

        if pathlib_available:
            self.assertEqual(str(Path(".")), str(_Path(".")))
            self.assertEqual(str(Path("./..")), str(_Path("./..")))
            self.assertEqual(str(Path("../..")), str(_Path("../..")))

    def test_method_repr(self):
        assert repr(Path(".")).endswith("Path('.')")
        assert repr(Path("/tmp/test")).endswith("Path('/tmp/test')")
        assert repr(Path("./sub_dir/file.txt")).endswith("Path('sub_dir/file.txt')")
        
        if pathlib_available:
            self.assertEqual(repr(Path(".")), repr(_Path(".")))
            self.assertEqual(repr(Path("/tmp/test")), repr(_Path("/tmp/test")))
            self.assertEqual(repr(Path("./sub_dir/file.txt")), repr(_Path("./sub_dir/file.txt")))

    def test_method_expanduser(self):
        if "HOME" in _os.environ.keys():
            self.assertEqual(str(Path("~").expanduser()), _os.environ["HOME"])
            
        if pathlib_available:
            self.assertEqual(str(Path("~").expanduser()), str(_Path("~").expanduser()))
            self.assertEqual(str(Path("~/tmp/test").expanduser()), str(_Path("~/tmp/test").expanduser()))
            self.assertEqual(str(Path("~/sub_dir/../file.txt").expanduser()), str(_Path("~/sub_dir/../file.txt").expanduser()))

    def test_method_exists(self):
        self.assertEqual(Path(".").exists(), 1 == 1)
        self.assertEqual(Path("..").exists(), 1 == 1)
        self.assertEqual(Path("/should/not/exist").exists(), 1 == 0)
        self.assertEqual(Path("~").expanduser().exists(), 1 == 1)
        

if __name__ == "__main__":
    _globals = globals()

    # Retrieve all the classes in the current file which are subclasses of `unittest.TestCase`.
    # Type `type` is necessary when developing with Python3 since all new-type classes have type `type` (search `<class 'type'>`)
    test_cases = [
        _globals[symbol]
        for symbol in _globals.keys()
        if type(_globals[symbol]).__name__
        in ["class", "type", "org.python.core.PyClass"]
        and issubclass(_globals[symbol], unittest.TestCase)
    ]

    # Find all the test methods from the classes found before and initialize the TestCase classes with those methods
    tests = [
        test_case(test_method) 
        for test_case in test_cases
        for test_method in dir(test_case)
        if test_method.startswith("test_")
        # and "showall" in test_method
    ]

    suite = unittest.TestSuite(tests)
    runner = unittest.TextTestRunner()

    # Start the tests
    runner.run(suite)
