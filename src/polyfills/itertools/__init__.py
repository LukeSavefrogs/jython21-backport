""" Polyfills for the `itertools` module. 

Usage:
    ```pycon
    >>> from polyfills import itertools
    >>> itertools.batched("Hello World", 3)
    ['Hel', 'lo ', 'Wor', 'ld']
    ```
"""
import unittest as _unittest

try:
    # If available, use `xrange` instead of `range`:
    # - On Python 2, `xrange` returns an iterator, while `range` returns a list.
    # - On Python 3, `xrange` does not exist, and `range` returns an iterator.
    range = xrange # pyright: ignore[reportUndefinedVariable]
except NameError:
    pass

def batched(iterable, length):
    # type: (str|list|tuple, int) -> list[str]
    """ Groups the specified string into chunks of the specified length.

    New in Python 3.12.

    Args:
        iterable (str|list|tuple): The iterable to group.
        length (int): The length of each chunk.

    Returns:
        chunks (list): A list of strings/tuples containing the chunks of the specified iterable.

    Examples:
        ```pycon
        >>> batched("Hello World", 3)
        ['Hel', 'lo ', 'Wor', 'ld']
        ```
    """
    batched_data = [
        iterable[i:i+length]
        for i in range(0, len(iterable), length)
    ]

    if type(iterable) in [type("")]:
        return batched_data

    return [tuple(_elem) for _elem in batched_data]


class BatchedTestCase(_unittest.TestCase):
    def test_string(self):
        self.assertEqual(batched("Hello World", 3), ['Hel', 'lo ', 'Wor', 'ld'])

    def test_list(self):
        flattened_data = ['roses', 'red', 'violets', 'blue', 'sugar', 'sweet']
        unflattened = list(batched(flattened_data, 2))
        
        self.assertEqual(
            unflattened,
            [('roses', 'red'), ('violets', 'blue'), ('sugar', 'sweet')],
        )

