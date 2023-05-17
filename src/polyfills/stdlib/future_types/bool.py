import unittest as _unittest

__all__ = ["bool"]

class bool:
    """ Backport of the boolean values (`True` and `False`), which were introduced in Python 2.3. """

    def __init__(self, value):
        # type: (int | str | list | dict | tuple | bool) -> None
        """ Returns True when the argument x is true, False otherwise. The
        builtins True and False are the only two instances of the class bool.
        The class bool is a subclass of the class int, and cannot be subclassed.
        """
        if type(value) == type(5) or type(value) == type(1 == 1):
            # -1 = True, 0 = False, 1 = True
            self.value = int(int(value) != 0) # type: ignore
        elif type(value) in [type(""), type(u""), type([]), type(()), type({})]:
            if value:
                self.value = 1
            else:
                self.value = 0
        elif type(value) == type(None):
            self.value = 0
        elif type(value) == type(self):
            self.value = int(value.value) # type: ignore
        else:
            raise TypeError("Type '%s' is not a valid boolean type" % type(value).__name__)

    def __repr__(self):
        if self.value == 1:
            return "True"
        else:
            return "False"
    
    def __str__(self):
        return self.__repr__()

    # Direct comparison (for if statements)
    def __nonzero__(self):
        return self.value == 1
    
    def __bool__(self):
        return self.value == 1

    # Rich comparison methods
    def __eq__(self, other):
        try:
            if other.__class__ == self.__class__:
                return self.value == other.value
        except:
            pass
        return self.value == other
    
    def __ne__(self, other):
        try:
            if other.__class__ == self.__class__:
                return self.value != other.value
        except:
            pass
        return self.value != other
    
    def __lt__(self, other):
        try:
            if other.__class__ == self.__class__:
                return self.value < other.value
        except:
            pass
        return self.value < other
    
    def __le__(self, other):
        try:
            if other.__class__ == self.__class__:
                return self.value <= other.value
        except:
            pass
        return self.value <= other
    
    def __gt__(self, other):
        try:
            if other.__class__ == self.__class__:
                return self.value > other.value
        except:
            pass
        return self.value > other
    
    def __ge__(self, other):
        try:
            if other.__class__ == self.__class__:
                return self.value >= other.value
        except:
            pass
        return self.value >= other

    # Boolean operations
    def __and__(self, other):
        try:
            if other.__class__ == self.__class__:
                return self.__class__(self.value and other.value)
        except:
            pass
        return self.__class__(self.value and other)
    
    def __or__(self, other):
        try:
            if other.__class__ == self.__class__:
                return self.__class__(self.value or other.value)
        except:
            pass
        return self.__class__(self.value or other)
    
    def __xor__(self, other):
        try:
            if other.__class__ == self.__class__:
                return self.__class__(self.value != other.value)
        except:
            pass
        return self.__class__(self.value != other)
    
    def __invert__(self):
        return self.__class__(not self.value)


# Locally, `True` and `False` are never redefined, since they are keywords.
try:
    (True, False)
except NameError:
    exec('True = bool(1); False = bool(0)')

    # Add `True` and `False` to the list of exported names.
    __all__ = ["bool", "True", "False"]


class _BooleanTestCase(_unittest.TestCase):
    """ Unit tests for the boolean type. """
    _True = bool(1)
    _False = bool(0)

    def test_native(self):
        self.assertEqual(1 == 1, self._True)
        self.assertEqual(1 == 0, self._False)
        self.assertEqual(self._True, 1 == 1)
        self.assertEqual(self._False, 1 == 0)
    
    def test_and(self):
        self.assertEqual(self._True and self._True, self._True)
        self.assertEqual(self._True and self._False, self._False)
        self.assertEqual(self._False and self._True, self._False)
        self.assertEqual(self._False and self._False, self._False)
    
    def test_or(self):
        self.assertEqual(self._True or self._True, self._True)
        self.assertEqual(self._True or self._False, self._True)
        self.assertEqual(self._False or self._True, self._True)
        self.assertEqual(self._False or self._False, self._False)
    
    def test_xor(self):
        self.assertEqual(self._True ^ self._True, self._False)
        self.assertEqual(self._True ^ self._False, self._True)
        self.assertEqual(self._False ^ self._True, self._True)
        self.assertEqual(self._False ^ self._False, self._False)
    
    def test_invert(self):
        self.assertEqual(~self._True, self._False)
        self.assertEqual(~self._False, self._True)
        self.assertEqual(~self._True, 1 == 0)
        self.assertEqual(~self._False, 1 == 1)

    def test_not(self):
        self.assertEqual(not self._True, self._False)
        self.assertEqual(not self._False, self._True)
        self.assertEqual(not self._True, 1 == 0)
        self.assertEqual(not self._False, 1 == 1)
    
    def test_nonzero(self):
        self.assertEqual(bool(self._True), 1)
        self.assertEqual(bool(self._False), 0)
    
    def test_eq(self):
        self.assertEqual(self._True, self._True)
        self.assertEqual(self._False, self._False)
        self.assertEqual(self._True, 1 == 1)
        self.assertEqual(self._False, 1 == 0)
        self.assertEqual(1 == 1, self._True)
        self.assertEqual(1 == 0, self._False)
    
    def test_ne(self):
        self.assertNotEqual(self._True, self._False)
        self.assertNotEqual(self._False, self._True)
        self.assertNotEqual(self._False, 1 == 1)
        self.assertNotEqual(self._True, 1 == 0)
        self.assertNotEqual(1 == 1, self._False)
        self.assertNotEqual(1 == 0, self._True)


if __name__ == '__main__':
    _globals = globals()

    # Retrieve all the classes in the current file which are subclasses of `unittest.TestCase`.
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
