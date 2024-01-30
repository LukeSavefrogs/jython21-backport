""" Collection of functions available natively in the standard library of
newer Python versions.
"""
from __future__ import nested_scopes

import sys as _sys
import unittest as _unittest

from polyfills.stdlib.future_types.bool import * # type: ignore # ==> Import the polyfills for boolean types

__all__ = [
    "sum",
    "sorted",
]

def enumerate(__iterable, start=0):
    """ It generates a sequence of tuples containing a count
    (from start which defaults to 0) and the values obtained from
    iterating over iterable.

    This is a backport of the Python `enumerate` built-in function
    (introduced in 2.3) that works down to Python 2.1 (tested).

    Args:
        __iterable (Iterable): The iterable to enumerate.
        start (int): The value to start from.

    Returns:
        enumerate (zip): An enumerate object.
    """
    try:
        range_func = xrange # pyright: ignore[reportUndefinedVariable]
    except NameError:
        range_func = range

    return zip(range_func(start, start + len(__iterable)), __iterable)

class EnumerateTestCase(_unittest.TestCase):
    def test_enumerate(self):
        """Test the `enumerate` function."""
        self.assertEqual(
            list(enumerate(["a", "b", "c"])),
            [(0, "a"), (1, "b"), (2, "c")],
            "Enumerate should work"
        )
        self.assertEqual(
            list(enumerate(["a", "b", "c"], 10)),
            [(10, "a"), (11, "b"), (12, "c")],
            "Enumerate should work with a start value"
        )

def sum(
    __iterable, # type: list[int|float]
    start = 0   # type: int
):
    """ Sums all the items in the iterable, starting from the `start` value.
    
    This is a backport of the Python `sum` built-in function (introduced in
    2.3) that works down to Python 2.1 (tested).
    
    Args:
        __iterable (list[int|float]): The iterable to sum.
        start (int): The value to start from.
        
    Returns:
        result (int|float): The sum of all the items in the iterable.
    """
    result = start

    for item in __iterable:
        result += item

    return result

def sorted(__iterable, key=None, reverse=False):
    """Return a new list containing all items from the iterable in ascending
    order.

    This is a backport of the Python `sorted` built-in function (introduced in
    2.4) that works down to Python 2.1 (tested).

    Args:
        item (Iterable): The iterable to sort (dictionary, tuple, list or string).
        key (function): The function to use to sort the items.
        reverse (bool): Whether to sort the items in reverse order.

    Returns:
        values (list): Ordered list with all the items of the original iterable.
    """
    item_type = type(__iterable)
    _dict, _list, _tuple, _str = type({}), type([]), type(()), type("")

    def key_to_cmp(key):
        """ Convert a key function to a cmp function. 
        
        Info: https://docs.python.org/3/howto/sorting.html#the-old-way-using-the-cmp-parameter
        """
        def cmp(a, b):
            """ The `cmp` function does not exist on Python 3.x.
            
            Source: https://stackoverflow.com/a/22490617/8965861
            """
            return (a > b) - (a < b) 

        # def cmp_func(x, y):
        #     if key(x) < key(y):
        #         return -1
        #     elif key(x) > key(y):
        #         return 1
        #     else:
        #         return 0
        # def cmp_func(x, y):
        #     return cmp(key(x), key(y))
        # return cmp_func
        return lambda x, y: cmp(key(x), key(y))
    
    # ---> List
    #
    #      When passed a list, the original `sorted` function
    #      sorts its elements as expected.
    if item_type == _list:
        elements = [elem for elem in __iterable]  # Make a copy of the original iterable

        if key is None:
            # If no key function is passed, sort the elements as they are
            elements.sort()
        else:
            # The `key` argument was introduced starting from Python 2.4
            if _sys.version_info >= (2, 4):
                elements.sort(key=key)
            else:
                # Convert the key function to a cmp function, since the `key` argument is not available.
                elements.sort(key_to_cmp(key))
        
        if reverse is True:
            elements.reverse()

        value = []
        for element in elements:
            if type(element) == _tuple:
                value.append(element)
            elif type(element) == _dict:
                value.append(element)
            elif type(element) == _list:
                value.append(sorted(element))
            else:
                value.append(element)

        return value

    # ---> Dictionary
    # 
    #      When passed a dictionary, the original `sorted` function
    #      sorts only its keys.
    elif item_type == _dict:
        return sorted([value for value in __iterable.keys()])

    # ---> Tuple
    #
    #      When passed a tuple, the original `sorted` function
    #      sorts its elements even if the tuple should be immutable.
    #       
    #      Example:
    #          >>> sorted((3, 2, 1))
    #          [1, 2, 3]
    elif item_type == _tuple:
        return sorted([value for value in __iterable])

    # ---> String
    #
    #      When passed a string, the original `sorted` function
    #      sorts its characters.
    elif item_type == _str:
        return sorted([char for char in __iterable])

    else:
        raise Exception(
            "Unhandled type '%s' for iterable '%s'" % (item_type, __iterable)
        )


class TestSum(_unittest.TestCase):
    def test_int_list(self):
        """Test summing a list of int."""
        self.assertEqual(sum([1, 2, 3]), 6)

    def test_int_tuple(self):
        """Test summing a tuple of int."""
        self.assertEqual(sum((1, 2, 3)), 6)

    def test_float_list(self):
        """Test summing a list of floats."""
        self.assertEqual(round(sum([1.1, 2.1, 3.1]), 1), 6.3)

    def test_float_tuple(self):
        """Test summing a tuple of floats."""
        self.assertEqual(round(sum((1.1, 2.1, 3.1)), 1), 6.3)


class _TestClass:
    def __init__(self, value):
        self.value = value
    
    def __eq__(self, __value):
        if type(__value) == self.__class__:
            return self.value == __value.value
        return self.value == __value

class TestSorted(_unittest.TestCase):
    def test_list(self):
        """Test sorting a list."""
        self.assertEqual(sorted([3, 2, 1]), [1, 2, 3])

    def test_list_of_lists(self):
        """Test sorting a list of lists."""
        self.assertEqual(sorted([[3, 2, 1], [2, 1, 3]]), [[1, 2, 3], [1, 2, 3]])

    def test_list_of_tuples(self):
        """Test sorting a list of tuples."""
        self.assertEqual(sorted([(3, 2, 1), (2, 1, 3)]), [(2, 1, 3), (3, 2, 1)])

    # def test_list_of_dicts(self):
    #     """Test sorting a list of dictionaries."""
    #     try:
    #         sorted([{3: 3, 2: 2, 1: 1}, {2: 2, 1: 1, 3: 3}])
    #     except TypeError:
    #         pass
    #     else:
    #         self.fail("TypeError not raised")

    def test_tuple(self):
        """Test sorting a tuple."""
        self.assertEqual(sorted((3, 2, 1)), [1, 2, 3])

    def test_tuple_of_lists(self):
        """Test sorting a tuple of lists."""
        self.assertEqual(sorted(([3, 2, 1], [2, 1, 3])), [[1, 2, 3], [1, 2, 3]])

    def test_tuple_of_tuples(self):
        """Test sorting a tuple of tuples."""
        self.assertEqual(sorted(((3, 2, 1), (2, 1, 3))), [(2, 1, 3), (3, 2, 1)])

    # def test_tuple_of_dicts(self):
    #     """Test sorting a tuple of dictionaries."""
    #     try:
    #         sorted(({3: 3, 2: 2, 1: 1}, {2: 2, 1: 1, 3: 3}))
    #     except TypeError:
    #         pass
    #     else:
    #         self.fail("TypeError not raised")

    def test_arg_key(self):
        """Test sorting a list with a key function."""
        self.assertEqual(sorted([-1, 3, 0, -13, 1, 2], key=lambda x: -x), [3, 2, 1, 0, -1, -13])
        self.assertEqual(
            sorted([{"key": 1}, {"key": 2}, {"key": 0}], key=lambda x: x["key"]),
            [{"key": 0}, {"key": 1}, {"key": 2}],
        )

        def cmp_func(x, y):
            if x.value < y.value:
                return -1
            elif x.value > y.value:
                return 1
            else:
                return 0

        self.assertEqual(
            # sorted([_TestClass(1), _TestClass(2), _TestClass(0)], key=cmp_func),
            sorted([_TestClass(1), _TestClass(2), _TestClass(0)], key=lambda x: x.value),
            [_TestClass(0), _TestClass(1), _TestClass(2)],
        )

    def test_arg_reverse(self):
        """Test sorting a list with a key function."""
        self.assertEqual(
            sorted([1, 3, 2], reverse=True),
            [3, 2, 1]
        )
        self.assertEqual(
            sorted([{"key": 1}, {"key": 2}, {"key": 0}], key=lambda x: x["key"], reverse=True),
            [{"key": 2}, {"key": 1}, {"key": 0}]
        )

        self.assertEqual(
            # sorted([_TestClass(1), _TestClass(2), _TestClass(0)], key=cmp_func, reverse=True),
            sorted([_TestClass(1), _TestClass(2), _TestClass(0)], key=lambda x: x.value, reverse=True),
            [_TestClass(2), _TestClass(1), _TestClass(0)],
        )

if __name__ == "__main__":
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
