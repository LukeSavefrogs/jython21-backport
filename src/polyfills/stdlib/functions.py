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
    "enumerate",
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

        return lambda x, y: cmp(key(x), key(y))
    
    class _ReverseCompare:
        """Wrapper class to reverse comparison for a single sort key component.
        
        This allows us to reverse only the primary sort key while keeping
        the secondary index-based key in normal order for stability.
        """
        def __init__(self, obj):
            self.obj = obj
        
        def __lt__(self, other):
            return self.obj > other.obj
        
        def __gt__(self, other):
            return self.obj < other.obj
        
        def __eq__(self, other):
            return self.obj == other.obj
        
        def __le__(self, other):
            return self.obj >= other.obj
        
        def __ge__(self, other):
            return self.obj <= other.obj
        
        def __ne__(self, other):
            return self.obj != other.obj
    
    # ---> List
    #
    #      When passed a list, the original `sorted` function
    #      sorts its elements as expected.
    if item_type == _list:
        # Make a copy and add original indices for stable sorting
        elements_with_index = [(i, elem) for i, elem in enumerate(__iterable)]

        if key is None:
            # If no key function is passed, sort the elements as they are
            # Add index as secondary sort key to ensure stability
            def stable_key(x):
                if reverse:
                    return (_ReverseCompare(x[1]), x[0])
                return (x[1], x[0])
            
            try:
                elements_with_index.sort(key=stable_key)
            except TypeError:
                # For very old Python versions without key support
                def stable_cmp(a, b):
                    result = (a[1] > b[1]) - (a[1] < b[1])
                    if reverse:
                        result = -result
                    if result == 0:
                        # If keys are equal, compare indices to maintain stability (never reverse index order)
                        result = (a[0] > b[0]) - (a[0] < b[0])
                    return result
                elements_with_index.sort(stable_cmp)
        else:
            # The `key` argument was introduced starting from Python 2.4
            # Wrap the key function to include the index for stability
            def stable_key_wrapper(x):
                if reverse:
                    return (_ReverseCompare(key(x[1])), x[0])
                return (key(x[1]), x[0])
            
            try:
                elements_with_index.sort(key=stable_key_wrapper)
            except TypeError:
                # Convert the key function to a `cmp` function for older Python versions
                # Include index comparison for stability
                def stable_cmp(a, b):
                    ka, kb = key(a[1]), key(b[1])
                    result = (ka > kb) - (ka < kb)
                    if reverse:
                        result = -result
                    if result == 0:
                        # If keys are equal, compare indices to maintain stability (never reverse index order)
                        result = (a[0] > b[0]) - (a[0] < b[0])
                    return result
                elements_with_index.sort(stable_cmp)
        
        # Extract just the elements (without indices)
        elements = [elem for _, elem in elements_with_index]

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

    def test_stability(self):
        """Test sorting a list multiple times to ensure stability.
        
        Demonstrates the idiom of sorting by secondary key first, then primary key.
        This leverages sort stability to achieve multi-key sorting.
        """
        # List of (name, section)
        data = [
            ("Dave", "A"),
            ("Alice", "B"),
            ("Ken", "A"),
            ("Eric", "B"),
            ("Carol", "A"),
        ]

        # First, sort by name (secondary key)
        data_sorted_by_name = sorted(data, key=lambda x: x[0])

        self.assertEqual(
            data_sorted_by_name,
            [
                ("Alice", "B"),
                ("Carol", "A"),
                ("Dave", "A"),
                ("Eric", "B"),
                ("Ken", "A"),
            ],
            "First sort by name should produce alphabetical order"
        )

        # Then, sort by section (primary key)
        # Since sort is stable, within each section the name order is preserved
        data_sorted_by_section = sorted(data_sorted_by_name, key=lambda x: x[1])

        self.assertEqual(
            data_sorted_by_section,
            [
                ("Carol", "A"),
                ("Dave", "A"),
                ("Ken", "A"),
                ("Alice", "B"),
                ("Eric", "B"),
            ],
            "Second sort by section should group by section while preserving name order within each section"
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
        and test_case.__name__.lower().find("sorted") != -1
    ]

    suite = _unittest.TestSuite(tests)
    runner = _unittest.TextTestRunner()

    # Start the tests
    runner.run(suite)
