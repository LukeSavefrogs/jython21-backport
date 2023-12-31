import unittest

class set:
    """ Return a new set or frozenset object whose elements are taken from iterable.
    The elements of a set must be hashable.
    If iterable is not specified, a new empty set is returned.
    """
    def __init__(self, iterable=None):
        self._set = []
        if iterable is not None:
            for item in iterable:
                self.add(item)

    def __contains__(self, item):
        """ Adds support for the following operation: `x in s` """
        return item in self._set

    def __len__(self):
        """ Adds support for the following operation: `len(s)` """
        return len(self._set)

    def add(self, item):
        if item not in self._set:
            self._set.append(item)

    def clear(self):
        self._set = []

    def copy(self):
        return set(self._set)

    def difference(self, other):
        return set([item for item in self._set if item not in other])

    def difference_update(self, other):
        self._set = self.difference(other)._set

    def discard(self, item):
        if item in self._set:
            self._set.remove(item)

    def intersection(self, *others):
        return set([
            item for item in self._set
            
            # Check if item is in all other sets
            if not [
                other_iterable
                for other_iterable in others
                if item not in other_iterable
            ]
        ])

    def intersection_update(self, other):
        self._set = self.intersection(other)._set

    def isdisjoint(self, other):
        return len(self.intersection(other)) == 0

    def issubset(self, other):
        return len(self.difference(other)) == 0

    def issuperset(self, other):
        return len(other.difference(self)) == 0

    # def pop(self):
    #     item = next(iter(self._set))
    #     del self._set[item]
    #     return item

    def remove(self, item):
        if item not in self._set:
            raise KeyError(item)
        self._set.remove(item)

    def symmetric_difference(self, other):
        return set([
            item for item in self._set if item not in other
        ]) | set([
            item for item in other._set if item not in self
        ])

    def symmetric_difference_update(self, other):
        self._set = self.symmetric_difference(other)._set

    def union(self, *others):
        # Convert all non-set iterables to sets first
        converted_others = [
            other for other in others
            if type(other) is set
        ] + [
            set(other) for other in others
            if type(other) is not set
        ]

        return set(self._set + [
            _elem
            for other in converted_others
            for _elem in other._set
        ])

    def update(self, *others):
        self._set = self.union(*others)._set

    def __repr__(self):
        return "{%s}" % ', '.join([
            type(item) == type("") and str("'%s'" % item) or str(item)
            for item in self._set
        ])
    
    def __eq__(self, other):
        set1 = self._set
        set2 = other._set

        if len(set1) != len(set2):
            return False
        
        set1.sort()
        set2.sort()

        return set1 == set2
    
    # Difference
    def __sub__(self, other):
        return self.difference(other)
    
    # Symmetric difference
    def __xor__(self, other):
        return self.symmetric_difference(other)
    
    # Subset
    def __lt__(self, other):
        return self.issubset(other) and self != other
    
    def __le__(self, other):
        return self.issubset(other)
    
    # Superset
    def __gt__(self, other):
        return self.issuperset(other) and self != other
    
    def __ge__(self, other):
        return self.issuperset(other)
    
    # Union
    def __or__(self, other):
        return self.union(other)
    
    # Intersection
    def __and__(self, other):
        return self.intersection(other)
    


class SetTests(unittest.TestCase):
    def test_length(self):
        # Testing an empty set
        self.assertEqual(len(set()), 0)

        # Testing a set with elements
        self.assertEqual(len(set(["apple", "orange", "banana"])), 3)

    def test_contains(self):
        # Creating a set
        fruits = set(["apple", "orange", "banana"])
        
        # Testing if a set contains an element
        self.assertTrue("apple" in fruits)
        self.assertTrue("pineapple" not in fruits)

    def test_subset(self):
        # Creating a set
        fruits = set(["apple", "orange", "banana"])

        # Testing if a set is a subset of another set
        self.assertTrue(set(["apple", "banana"]).issubset(fruits))
        self.assertFalse(set(["apple", "pineapple"]).issubset(fruits))

        # Testing if a set is a proper subset of another set
        self.assertFalse(set(["apple", "pineapple"]) <= fruits)
        self.assertTrue(set(["apple", "banana"]) <= fruits)
        self.assertTrue(fruits <= fruits)

        # Testing if a set is a proper subset of another set
        self.assertFalse(set(["apple", "orange", "banana"]) < fruits)
        self.assertTrue(set(["apple", "banana"]) < fruits)

    def test_superset(self):
        # Creating a set
        fruits = set(["apple", "orange", "banana"])

        # Testing if a set is a superset of another set
        self.assertTrue(fruits.issuperset(set(["apple", "banana"])))
        self.assertFalse(fruits.issuperset(set(["apple", "pineapple"])))

        # Testing if a set is a proper superset of another set
        self.assertFalse(fruits >= set(["apple", "pineapple"]))
        self.assertTrue(fruits >= set(["apple", "banana"]))
        self.assertTrue(fruits >= fruits)

        # Testing if a set is a proper superset of another set
        self.assertFalse(fruits > set(["apple", "orange", "banana"]))
        self.assertTrue(fruits > set(["apple", "banana"]))
    
    def test_add(self):
        # Adding an element to an empty set
        empty_set = set()
        empty_set.add("apple")
        self.assertEqual(len(empty_set), 1)

        # Adding an element to a set
        fruits = set(["apple", "orange"])
        fruits.add("banana")
        self.assertEqual(len(fruits), 3)

    def test_remove(self):
        # Removing an existing element from a set
        fruits = set(["apple", "orange", "banana"])
        fruits.remove("banana")
        self.assertEqual(len(fruits), 2)

        # Trying to remove an element that doesn't exist
        empty_set = set()
        with self.assertRaises(KeyError):
            empty_set.remove("apple")

    def test_union(self):
        # Creating two sets
        fruits1 = set(["apple", "orange"])
        fruits2 = set(["banana", "grape"])

        # Combining two sets using union()
        united_fruits = fruits1 | fruits2
        self.assertEqual(united_fruits, set(["apple", "banana", "grape", "orange"]))

        # Combining multiple sets using union()
        united_fruits = fruits1 | fruits2 | set(["pineapple"])
        self.assertEqual(united_fruits, set(["apple", "banana", "grape", "orange", "pineapple"]))

        # Test union with different types
        united_fruits = fruits1.union(fruits2, ["pineapple"], 'as')
        self.assertEqual(united_fruits, set(["apple", "banana", "grape", "orange", "pineapple", "a", "s"]))

    def test_intersection(self):
        # Creating two sets
        fruits1 = set(["apple", "orange", "pineapple"])
        fruits2 = set(["orange", "banana", "grape"])

        # Finding common elements using intersection()
        intersecting_fruits = fruits1 & fruits2
        self.assertEqual(intersecting_fruits, set(["orange"]))

        # Finding common elements in multiple sets using intersection()
        intersecting_fruits = fruits1 & fruits2 & set(["pineapple"])
        self.assertEqual(intersecting_fruits, set([]))

        intersecting_fruits = fruits1 & fruits2 & set(["orange"])
        self.assertEqual(intersecting_fruits, set(["orange"]))

        self.assertEqual(set('abc').intersection('cbs'), set(["c", "b"]))

    def test_difference(self):
        # Creating two sets
        fruits1 = set(["apple", "orange", "pineapple"])
        fruits2 = set(["orange", "banana", "grape"])

        # Finding elements unique to each set using difference()
        self.assertEqual(fruits1 - fruits2, set(["apple", "pineapple"]))
        self.assertEqual(fruits2 - fruits1, set(["banana", "grape"]))

        self.assertEqual(fruits1.difference(fruits2), set(["apple", "pineapple"]))
        self.assertEqual(fruits2.difference(fruits1), set(["banana", "grape"]))


    def test_symmetric_difference(self):
        # Creating two sets
        fruits1 = set(["apple", "orange", "pineapple"])
        fruits2 = set(["orange", "banana", "grape"])

        # Finding elements unique to each set using symmetric_difference()
        self.assertEqual(fruits1 ^ fruits2, set(["apple", "banana", "grape", "pineapple"]))
        self.assertEqual(fruits1.symmetric_difference(fruits2), set(["apple", "banana", "grape", "pineapple"]))

    def test_clear(self):
        # Creating a set
        fruits = set(["apple", "orange", "banana"])

        # Clearing a set
        fruits.clear()
        self.assertEqual(len(fruits), 0)

    def test_copy(self):
        # Creating a set
        fruits = set(["apple", "orange", "banana"])

        # Copying a set
        self.assertEqual(fruits.copy(), set(["apple", "orange", "banana"]))

    def test_update(self):
        # Creating a set
        fruits = set(["apple", "orange", "banana"])

        # Updating a set
        fruits.update(set(["pineapple"]))
        self.assertEqual(fruits, set(["apple", "orange", "banana", "pineapple"]))

        fruits.update(["pineapple"], ["grape"])
        self.assertEqual(fruits, set(["apple", "orange", "banana", "pineapple", "grape"]))   

if __name__ == '__main__':
    unittest.main()
