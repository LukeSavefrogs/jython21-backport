import unittest as _unittest

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

def sorted(__iterable):
    """Return a new list containing all items from the iterable in ascending
    order.

    This is a backport of the Python `sorted` built-in function (introduced in
    2.4) that works down to Python 2.1 (tested).

    Args:
        item (Iterable): The iterable to sort (dictionary, tuple, list or string).

    Returns:
        values (list): Ordered list with all the items of the original iterable.
    """
    item_type = type(__iterable)
    _dict, _list, _tuple, _str = type({}), type([]), type(()), type("")
    
    # ---> List
    #
    #      When passed a list, the original `sorted` function
    #      sorts its elements as expected.
    if item_type == _list:
        elements = [elem for elem in __iterable]  # Make a copy of the original iterable
        elements.sort()

        value = []
        for element in elements:
            if type(element) == _tuple:
                value.append(element)
            elif type(element) == _dict:
                raise TypeError(
                    "unorderable types: dict() < dict() (not supported in Python 2.1)"
                )
            elif type(element) in [_list, _dict, _tuple]:
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

    def test_list_of_dicts(self):
        """Test sorting a list of dictionaries."""
        try:
            sorted([{3: 3, 2: 2, 1: 1}, {2: 2, 1: 1, 3: 3}])
        except TypeError:
            pass
        else:
            self.fail("TypeError not raised")

    def test_tuple(self):
        """Test sorting a tuple."""
        self.assertEqual(sorted((3, 2, 1)), [1, 2, 3])

    def test_tuple_of_lists(self):
        """Test sorting a tuple of lists."""
        self.assertEqual(sorted(([3, 2, 1], [2, 1, 3])), [[1, 2, 3], [1, 2, 3]])

    def test_tuple_of_tuples(self):
        """Test sorting a tuple of tuples."""
        self.assertEqual(sorted(((3, 2, 1), (2, 1, 3))), [(2, 1, 3), (3, 2, 1)])

    def test_tuple_of_dicts(self):
        """Test sorting a tuple of dictionaries."""
        try:
            sorted(({3: 3, 2: 2, 1: 1}, {2: 2, 1: 1, 3: 3}))
        except TypeError:
            pass
        else:
            self.fail("TypeError not raised")


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
