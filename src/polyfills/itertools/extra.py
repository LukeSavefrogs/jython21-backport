""" This module contains a subset of features from the `more_itertools` package. """
import unittest as _unittest
from polyfills.itertools import batched

try:
    # If available, use `xrange` instead of `range`:
    # - On Python 2, `xrange` returns an iterator, while `range` returns a list.
    # - On Python 3, `xrange` does not exist, and `range` returns an iterator.
    range = xrange # pyright: ignore[reportUndefinedVariable]
except NameError:
    pass


def chunked(iterable, length):
    """ Groups the specified string into chunks of the specified length. 
    
    Alias used by the `more_itertools` package for `batched`.

    Args:
        iterable (str|list|tuple): The iterable to group.
        length (int): The length of each chunk.

    Returns:
        chunks (list): A list of strings/tuples containing the chunks of the specified iterable.
    """
    return batched(iterable, length)

class ChunkedTestCase(_unittest.TestCase):
    def test_string(self):
        self.assertEqual(chunked("Hello World", 3), ['Hel', 'lo ', 'Wor', 'ld'])

    def test_list(self):
        flattened_data = ['roses', 'red', 'violets', 'blue', 'sugar', 'sweet']
        unflattened = list(chunked(flattened_data, 2))
        
        self.assertEqual(
            unflattened,
            [('roses', 'red'), ('violets', 'blue'), ('sugar', 'sweet')],
        )


def flatten(iterable):
    # type: (list[list]) -> list
    """ Flattens a list of lists into a single list.

    From the `more_itertools` package.

    Args:
        iterable (list[list]): The list of lists to flatten.

    Returns:
        flattened (list): A list containing the elements of the specified list of lists.

    Examples:
        ```pycon
        >>> flatten([[1, 2, 3], [4, 5, 6]])
        [1, 2, 3, 4, 5, 6]
        ```
    """
    return [
        item
        for sublist in iterable
        for item in sublist
    ]

class FlattenTestCase(_unittest.TestCase):
    def test_flatten(self):
        iterable = [(0, 1), (2, 3)]
        
        self.assertEqual(
            list(flatten(iterable)),
            [0, 1, 2, 3],
        )
    
    def test_nested_iterables(self):
        iterable = [(0, 1), [(2, 3), (4, 5)]]
        
        self.assertEqual(
            list(flatten(iterable)),
            [0, 1, (2, 3), (4, 5)],
        )

if __name__ == '__main__':
    _unittest.main()