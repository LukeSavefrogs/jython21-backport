""" Not all `os.path` methods are available for Jython.

```
wsadmin>dir(os.path)
['File', 'System', '__doc__', '__file__', '__name__', '_tostr', 'abspath', 'basename', 'commonprefix', 'dirname', 'exists', 'expanduser', 'expandvars', 'getatime', 'gethome', 'getmtime', 'getsize', 'getuser', 'isabs', 'isdir', 'isfile', 'islink', 'ismount', 'java', 'join', 'normcase', 'normpath', 'os', 'samefile', 'split', 'splitdrive', 'splitext', 'walk']
```
"""
import os as _os
import glob as _glob
import unittest as _unittest

try:
    from pathlib import Path as _Path
except ImportError:
    pathlib_available = 0
else: 
    pathlib_available = 1


__all__ = ["Path"]

class _Flavour:
    """A flavour implements a particular (platform-specific) set of path
    semantics."""  

    def __init__(self):
        self.join = self.sep.join

class _WindowsFlavour(_Flavour):
    # Reference for Windows paths can be found at
    # http://msdn.microsoft.com/en-us/library/aa365247%28v=vs.85%29.aspx
    name = "Windows"
    """ Name of the flavour. """

    sep = '\\'
    """ Path separator. """

    altsep = '/'
    """ Alternate pathname separator. """

    has_drv = 1 == 1

    is_supported = (_os.name == 'nt')
    """ Wether the flavour is supported on the current platform. """
class _PosixFlavour(_Flavour):
    name = "Posix"
    """ Name of the flavour. """

    sep = '/'
    """ Path separator. """

    altsep = ''
    """ Alternate pathname separator. """

    has_drv = 1 == 0

    is_supported = (_os.name != 'nt')
    """ Wether the flavour is supported on the current platform. """ 


class Path:
    _path = ""
    _flavour = None

    def __init__(self, *args, **kwargs):
        exec("import os as _os")
        if _os.name == 'nt':
            self._flavour = _WindowsFlavour()
            self._path = _os.path.join(*args).replace("/", "\\")
        else:
            self._flavour = _PosixFlavour()
            self._path = _os.path.join(*args)
        
        if self._path.replace("\\", "/").startswith("./"):
            self._path = self._path[2:]
        
    def __str__(self):
        return str(self._path)
    
    def __repr__(self):
        return "%s('%s')" % (self._flavour.name + "Path", str(self._path).replace("\\", "/"))
    
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
    
    def as_posix(self):
        """ Return the string representation of the path with forward slashes (`/`).
        
        Returns:
            str: The string representation of the path with forward slashes (`/`).
        """
        return str(self).replace(self._flavour.sep, '/')

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
        """ Expand ~ and ~user constructions. If user or $HOME is unknown, do nothing. 

        Returns:
            Path: A new 'Path' object with the expanded user path.
        """        
        return Path(_os.path.expanduser(self._path))

    # WORKS
    def exists(self):
        """ Whether this path exists.

        Returns:
            bool: True if the path exists, False otherwise. 
        """
        return _os.path.exists(str(Path(self._path).resolve()))

    def glob(self, pattern):
        """ Iterate over this subtree and yield all existing files (of any
        kind, including directories) matching the given relative pattern.

        Args:
            pattern (str): The pattern to match against.

        Returns:
            list: A list of 'Path' objects matching the pattern.
        """
        pattern = Path(self._path).resolve() / pattern
        
        return _glob.glob(pattern)
    
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


class PathTestCase(_unittest.TestCase):
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

    # Retrieve all the classes in the current file which are subclasses of `_unittest.TestCase`.
    # Type `type` is necessary when developing with Python3 since all new-type classes have type `type` (search `<class 'type'>`)
    test_cases = [
        _globals[symbol]
        for symbol in _globals.keys()
        if type(_globals[symbol]).__name__
        in ["class", "type", "org.python.core.PyClass"]
        and issubclass(_globals[symbol], _unittest.TestCase)
    ]

    # Find all the test methods from the classes found before and initialize the TestCase classes with those methods
    tests = [
        test_case(test_method) 
        for test_case in test_cases
        for test_method in dir(test_case)
        if test_method.startswith("test_")
        # and "showall" in test_method
    ]

    suite = _unittest.TestSuite(tests)
    runner = _unittest.TextTestRunner()

    # Start the tests
    runner.run(suite)
