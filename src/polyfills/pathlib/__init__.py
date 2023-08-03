""" Not all `os.path` methods are available for Jython.

```
wsadmin>dir(os.path)
['File', 'System', '__doc__', '__file__', '__name__', '_tostr', 'abspath', 'basename', 'commonprefix', 'dirname', 'exists', 'expanduser', 'expandvars', 'getatime', 'gethome', 'getmtime', 'getsize', 'getuser', 'isabs', 'isdir', 'isfile', 'islink', 'ismount', 'java', 'join', 'normcase', 'normpath', 'os', 'samefile', 'split', 'splitdrive', 'splitext', 'walk']
```
"""
import os as _os
import glob as _glob
import time
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


class _WindowsFlavour(_Flavour):
    """Implements Windows path semantics."""

    # Reference for Windows paths can be found at
    # http://msdn.microsoft.com/en-us/library/aa365247%28v=vs.85%29.aspx
    name = "Windows"
    """ Name of the flavour. """

    sep = "\\"
    """ Path separator. """

    altsep = "/"
    """ Alternate pathname separator. """

    has_drv = 1 == 1

    is_supported = _os.name == "nt"
    """ Wether the flavour is supported on the current platform. """


class _PosixFlavour(_Flavour):
    """Implements Posix path semantics."""

    name = "Posix"
    """ Name of the flavour. """

    sep = "/"
    """ Path separator. """

    altsep = ""
    """ Alternate pathname separator. """

    has_drv = 1 == 0

    is_supported = _os.name != "nt"
    """ Wether the flavour is supported on the current platform. """


class Base:
    pass


class Path(Base):
    """Represents a path to a file or directory.

    Polyfill for `pathlib.Path` for Jython.
    """

    _path = ""
    _flavour = None

    def __init__(self, *args, **kwargs):
        # Ensure the os module is always loaded, even if the class is copied
        exec("import os as _os")
        if _os.name == "nt":
            self._flavour = _WindowsFlavour()
            self._path = _os.path.join(*args).replace("/", self._flavour.sep)
        else:
            self._flavour = _PosixFlavour()
            self._path = _os.path.join(*args)

        if self.as_posix().startswith("./"):
            self._path = self._path[2:]

        # Remove the final path if it references the current folder
        if self.as_posix().endswith("/."):
            self._path = self._path[:-2]

        # Remove excess trailing slashes, except when the path is the root
        while self.as_posix().endswith("/") and self.as_posix() not in ["/", "//"]:
            self._path = self._path[:-1]

    def __str__(self):
        return str(self._path)

    def __repr__(self):
        return "%s('%s')" % (
            self._flavour.name + "Path",
            str(self._path).replace("\\", "/"),
        )

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

    # The `__getattribute__` magic method is not present in Python 2.1
    def __getattr__(self, name):
        """`__getattr__` gets called every time an undefined attribute is accessed.

        We use this to implement the `parent`, `name`, `stem` and `suffix` properties.

        Args:
            name (str): The name of the attribute to get.
        """
        if name == "parent":
            # `.` and `..` are actually children of the current folder (`.`)
            if self.as_posix() in [".", ".."]:
                return Path(".")

            parent_folder = _os.path.dirname(str(self))
            return Path(parent_folder)

        elif name == "name":
            return _os.path.basename(str(self))

        elif name == "stem":  # Return the name of the file
            """Return the final path component, without its suffix, if any.
            CPython 3.9.6:
            >>> os.path.splitext("..")
            ('..', '')

            Jython 2.1:
            >>> os.path.splitext("..")
            ('.', '.')
            """
            basename = _os.path.basename(str(self))

            if basename == ".":
                return ""
            elif basename == "..":
                return ".."

            return _os.path.splitext(basename)[0]

        elif name == "suffix":  # Return the extension of the file
            basename = _os.path.basename(str(self))
            suffix = Path(basename).as_posix().split("/")[-1]

            if suffix in [".", ".."]:
                return ""

            return _os.path.splitext(basename)[1]

        else:
            return Base.__getattr__(self, name)

    def as_posix(self):
        """Return the string representation of the path with forward slashes (`/`).

        Returns:
            str: The string representation of the path with forward slashes (`/`).
        """
        return str(self).replace("\\", "/")

    def absolute(self):
        """Return an absolute version of this path.  This function works
        even if the path doesn't point to anything.

        No normalization is done, i.e. all '.' and '..' will be kept along.
        Use resolve() to get the canonical path to a file.

        Returns:
            Path: A new 'Path' object with the absolute path.
        """
        parts = self._path.replace("\\", "/").split("/")
        if parts[-1].strip() == "":
            parts.pop()

        if parts[0] == ".":
            self._path = _os.path.join(_os.path.abspath("."), *parts[1:])

        return Path(self._path)

    # WORKS (needs testing for symlinks)
    def resolve(self):
        """Make the path absolute, resolving all symlinks on the way and also
        normalizing it (for example turning slashes into backslashes under
        Windows).

        Returns:
            Path: A new 'Path' object with the resolved path.
        """
        return Path(_os.path.abspath(_os.path.normpath(self._path)))

    def expanduser(self):
        """Expand ~ and ~user constructions. If user or $HOME is unknown, do nothing.

        Returns:
            Path: A new 'Path' object with the expanded user path.
        """
        return Path(_os.path.expanduser(self._path))

    def exists(self):
        """Whether this path exists.

        Returns:
            bool: True if the path exists, False otherwise.
        """
        return _os.path.exists(str(Path(self._path).resolve()))

    def glob(self, pattern):
        """Iterate over this subtree and yield all existing files (of any
        kind, including directories) matching the given relative pattern.

        Args:
            pattern (str): The pattern to match against.

        Returns:
            list: A list of 'Path' objects matching the pattern.
        """
        pattern = Path(self._path).resolve() / pattern

        return _glob.glob(pattern)

    def unlink(self, missing_ok=1 == 0):
        """Remove this file or link.  If the path is a directory, use rmdir() instead.

        Raises:
            OSError: If the path is a directory and `missing_ok` is False.

        Returns:
            None: No return value.
        """
        try:
            _os.remove(str(Path(self._path).resolve()))
        except FileNotFoundError:
            if not missing_ok:
                raise

    def read_bytes(self):
        """Open the file in bytes mode, read it, and close the file.

        Returns:
            bytes: The data read from the file.
        """
        return self._safe_read(self._path, mode="rb")

    def read_text(self, mode="r"):
        """Open the file in text mode, read it, and close the file.

        Returns:
            str: The data read from the file.
        """
        return self._safe_read(self._path, mode="r")

    def write_bytes(self, data):
        """Open the file in bytes mode, write to it, and close the file.

        Args:
            data (bytes): The data to write to the file.

        Returns:
            None: No return value.
        """
        self._safe_write(self._path, data, mode="wb")

    def write_text(self, data):
        """Open the file in text mode, write to it, and close the file.

        Args:
            data (str): The data to write to the file.

        Returns:
            None: No return value.
        """
        self._safe_write(self._path, data, mode="w")

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

    def is_file(self):
        """Whether this path is a file.

        Returns:
            bool: True if the path is a file, False otherwise.
        """
        return _os.path.isfile(str(self.resolve()))

    def is_dir(self):
        """Whether this path is a directory.

        Returns:
            bool: True if the path is a directory, False otherwise.
        """
        return _os.path.isdir(str(self.resolve()))


class PathTestCase(_unittest.TestCase):
    def test_creation(self):
        self.assertEqual(
            str(Path("/", "tmp", "", "test.py")), "%stmp%stest.py" % (_os.sep, _os.sep)
        )
        self.assertEqual(
            str(Path("/tmp/test.py")), "%stmp%stest.py" % (_os.sep, _os.sep)
        )

    def test_dots(self):
        self.assertEqual(str(Path(".")), ".")
        self.assertEqual(str(Path("./..")), "..")
        self.assertEqual(str(Path("../..")), "..%s.." % (_os.sep))

        if pathlib_available:
            self.assertEqual(str(Path(".")), str(_Path(".")))
            self.assertEqual(str(Path("./..")), str(_Path("./..")))
            self.assertEqual(str(Path("../..")), str(_Path("../..")))

    def test_method_as_posix(self):
        self.assertEqual(Path("/tmp/file.txt").as_posix(), "/tmp/file.txt")
        self.assertEqual(Path("\\tmp\\file.txt").as_posix(), "/tmp/file.txt")
        self.assertEqual(
            Path("C:\\Users\\MyUser\\Desktop").as_posix(), "C:/Users/MyUser/Desktop"
        )
        self.assertEqual(Path("\\Path\\To\\Resource").as_posix(), "/Path/To/Resource")

    def test_method_repr(self):
        assert repr(Path(".")).endswith("Path('.')")
        assert repr(Path("/tmp/test")).endswith("Path('/tmp/test')")
        assert repr(Path("./sub_dir/file.txt")).endswith("Path('sub_dir/file.txt')")

        if pathlib_available:
            self.assertEqual(repr(Path(".")), repr(_Path(".")))
            self.assertEqual(repr(Path("/tmp/test")), repr(_Path("/tmp/test")))
            self.assertEqual(
                repr(Path("./sub_dir/file.txt")), repr(_Path("./sub_dir/file.txt"))
            )

    def test_method_str(self):
        self.assertEqual(str(Path("/tmp").as_posix()), "/tmp")
        self.assertEqual(str(Path("/tmp/").as_posix()), "/tmp")
        self.assertEqual(str(Path("/tmp/file.py").as_posix()), "/tmp/file.py")
        self.assertEqual(str(Path("/tmp/file.py//").as_posix()), "/tmp/file.py")

    def test_method_expanduser(self):
        if "HOME" in _os.environ.keys():
            self.assertEqual(str(Path("~").expanduser()), _os.environ["HOME"])

        if pathlib_available:
            self.assertEqual(str(Path("~").expanduser()), str(_Path("~").expanduser()))
            self.assertEqual(
                str(Path("~/tmp/test").expanduser()),
                str(_Path("~/tmp/test").expanduser()),
            )
            self.assertEqual(
                str(Path("~/sub_dir/../file.txt").expanduser()),
                str(_Path("~/sub_dir/../file.txt").expanduser()),
            )

    def test_method_exists(self):
        self.assertEqual(Path(".").exists(), 1 == 1)
        self.assertEqual(Path("..").exists(), 1 == 1)
        self.assertEqual(Path("/should/not/exist").exists(), 1 == 0)
        self.assertEqual(Path("~").expanduser().exists(), 1 == 1)

    def test_property_parent(self):
        self.assertEqual(Path(".").parent.as_posix(), ".")
        self.assertEqual(Path("..").parent.as_posix(), ".")
        self.assertEqual(Path("/tmp").parent.as_posix(), "/")
        self.assertEqual(Path("/tmp/test").parent.as_posix(), "/tmp")
        self.assertEqual(Path("/tmp/test/").parent.as_posix(), "/tmp")
        self.assertEqual(Path("/tmp/test/.").parent.as_posix(), "/tmp")
        self.assertEqual(Path("/tmp/test/..").parent.as_posix(), "/tmp/test")
        self.assertEqual(Path("/tmp/test/../").parent.as_posix(), "/tmp/test")

    def test_property_name(self):
        self.assertEqual(str(Path(".").name), ".")
        self.assertEqual(str(Path("..").name), "..")
        self.assertEqual(str(Path("/tmp").name), "tmp")
        self.assertEqual(str(Path("/tmp/test").name), "test")
        self.assertEqual(str(Path("/tmp/test/").name), "test")
        self.assertEqual(str(Path("/tmp/test/..").name), "..")
        self.assertEqual(str(Path("/tmp/test/../").name), "..")
        self.assertEqual(str(Path("/tmp/test/.").name), "test")

    def test_property_stem(self):
        self.assertEqual(str(Path(".").stem), "")
        self.assertEqual(str(Path("..").stem), "..")
        self.assertEqual(str(Path("/tmp").stem), "tmp")
        self.assertEqual(str(Path("/tmp/test").stem), "test")
        self.assertEqual(str(Path("/tmp/test/").stem), "test")
        self.assertEqual(str(Path("/tmp/test/..").stem), "..")
        self.assertEqual(str(Path("/tmp/test/../").stem), "..")
        self.assertEqual(str(Path("/tmp/test/.").stem), "test")

    def test_property_suffix(self):
        self.assertEqual(str(Path(".").suffix), "")
        self.assertEqual(str(Path("..").suffix), "")
        self.assertEqual(str(Path("/tmp").suffix), "")
        self.assertEqual(str(Path("/tmp/test").suffix), "")
        self.assertEqual(str(Path("/tmp/test/").suffix), "")
        self.assertEqual(str(Path("/tmp/test/..").suffix), "")
        self.assertEqual(str(Path("/tmp/test/../").suffix), "")
        self.assertEqual(str(Path("/tmp/test/.").suffix), "")
        self.assertEqual(str(Path("/tmp/test.txt").suffix), ".txt")
        self.assertEqual(str(Path("/tmp/test.txt/").suffix), ".txt")
        self.assertEqual(str(Path("/tmp/test.txt/..").suffix), "")
        self.assertEqual(str(Path("/tmp/test.txt/../").suffix), "")
        self.assertEqual(str(Path("/tmp/test.txt/.").suffix), ".txt")
        self.assertEqual(str(Path("/tmp/test.txt.tar.gz").suffix), ".gz")
        self.assertEqual(str(Path("/tmp/test.txt.tar.gz/").suffix), ".gz")
        self.assertEqual(str(Path("/tmp/test.txt.tar.gz/..").suffix), "")
        self.assertEqual(str(Path("/tmp/test.txt.tar.gz/../").suffix), "")
        self.assertEqual(str(Path("/tmp/test.txt.tar.gz/.").suffix), ".gz")

    def test_is_dir(self):
        self.assertEqual(Path(".").is_dir(), 1 == 1)
        self.assertEqual(Path("..").is_dir(), 1 == 1)

    def test_is_file(self):
        self.assertEqual(Path(".").is_file(), 1 == 0)
        self.assertEqual(Path("..").is_file(), 1 == 0)
        self.assertEqual(Path("README.md").is_file(), 1 == 1)
        self.assertEqual(
            Path("src", "polyfills", "pathlib", "__init__.py").is_file(), 1 == 1
        )


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
