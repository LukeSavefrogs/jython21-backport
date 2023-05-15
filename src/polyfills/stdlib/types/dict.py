import sys as _sys
import unittest as _unittest


# TODO: Check if `class dict(type({}))` works:
class dict:
    def __init__(self, *args, **kwargs):
        self.__dict__ = {}

        # Needs to be thoroughly tested
        self.__class__.__name__ = type({}).__name__

        # Prior to Python 3.3 was possible to override the type of the class
        try:
            self.__class__ = type({})
        except TypeError:
            pass

        for k, v in kwargs.items():
            self.__dict__[k] = v

        if len(args) > 1:
            raise TypeError("dict expected at most 1 argument, got %d" % len(args))
        
        for arg in args:
            if type(arg) == type({}):
                for k, v in arg.items():
                    self.__dict__[k] = v
            elif type(arg) in [type([]), type(())]:
                for kv_pair in arg:
                    if type(kv_pair) in [type([]), type(())]:
                        self.__dict__[kv_pair[0]] = kv_pair[1]
                    else:
                        raise ValueError("Type '%s' is not a valid pair type" % type(kv_pair).__name__)
            else:
                raise ValueError("Type '%s' is not a valid dict type" % type(arg).__name__)
    

    def __contains__(self, key):
        return self.__dict__.__contains__(key)

    def __delattr__(self, key):
        return self.__dict__.__delattr__(key)

    def __delitem__(self, *args, **kwargs):
        return self.__dict__.__delitem__(*args, **kwargs)
        

    def __dir__(self, *args, **kwargs):
        return self.__dict__.__dir__(*args, **kwargs)


    def __eq__(self, other):
        if type(other) == type(self):
            return self.__dict__ == other.__dict__
        return self.__dict__ == other

    def __ne__(self, other):
        if type(other) == type(self):
            return self.__dict__ != other.__dict__
        return self.__dict__ != other

    def __len__(self):
        return self.__dict__.__len__()

    # Ordering methods are not supported for dicts
    #
    # >>> {"a": 1} > {"a": 0}
    # Traceback (most recent call last):
    # File "<stdin>", line 1, in <module>
    # TypeError: '>' not supported between instances of 'dict' and 'dict'
    #
    # def __gt__(self, *args, **kwargs):
    #     return self.__dict__.__gt__(*args, **kwargs)

    # def __ge__(self, *args, **kwargs):
    #     return self.__dict__.__ge__(*args, **kwargs)

    # def __le__(self, *args, **kwargs):
    #     return self.__dict__.__le__(*args, **kwargs)

    # def __lt__(self, *args, **kwargs):
    #     return self.__dict__.__lt__(*args, **kwargs)



    # String conversions
    def __str__(self):
        return self.__dict__.__str__()

    def __repr__(self):
        return self.__dict__.__repr__()



    def __getitem__(self, key):
        return self.__dict__.__getitem__(key)
        
    def __setitem__(self, key, value):
        return self.__dict__.__setitem__(key, value)


    def __format__(self, *args, **kwargs):
        return self.__dict__.__format__(*args, **kwargs)
    
    def __ior__(self, *args, **kwargs):
        return self.__dict__.__ior__(*args, **kwargs)

    def __iter__(self, *args, **kwargs):
        return self.__dict__.__iter__(*args, **kwargs)

    def __or__(self, *args, **kwargs):
        return self.__dict__.__or__(*args, **kwargs)

    def __reduce__(self, *args, **kwargs):
        return self.__dict__.__reduce__(*args, **kwargs)

    def __reduce_ex__(self, *args, **kwargs):
        return self.__dict__.__reduce_ex__(*args, **kwargs)

    def __reversed__(self, *args, **kwargs):
        return self.__dict__.__reversed__(*args, **kwargs)

    def __ror__(self, *args, **kwargs):
        return self.__dict__.__ror__(*args, **kwargs)

    def __sizeof__(self, *args, **kwargs):
        return self.__dict__.__sizeof__(*args, **kwargs)

    def __subclasshook__(self, *args, **kwargs):
        return self.__dict__.__subclasshook__(*args, **kwargs)

    def clear(self):
        return self.__dict__.clear()

    def copy(self):
        return self.__dict__.copy()

    def fromkeys(seq, value=None):
        if "fromkeys" not in dir({}):
            raise AttributeError("{}.fromkeys() is not implemented")
        
        return {}.fromkeys(seq, value)

    def get(self, key, default=None):
        return self.__dict__.get(key, default)

    def items(self, *args, **kwargs):
        return self.__dict__.items(*args, **kwargs)

    def keys(self, *args, **kwargs):
        return self.__dict__.keys(*args, **kwargs)

    def pop(self, *args, **kwargs):
        return self.__dict__.pop(*args, **kwargs)

    def popitem(self):
        return self.__dict__.popitem()

    def setdefault(self, key, default=None):
        """ If key is in the dictionary, return its value. 
        
        If not, insert key with a value of `default` and return `default`.

        Args:
            key (str): The key of the dictionary
            default (typing.Any, optional): The default value, will be used if the key is not in the dictionary. Defaults to None.

        Returns:
            typing.Any: The value of the item in the dictionary.
        """
        return self.__dict__.setdefault(key, default)

    def update(self, *args, **kwargs):
        """ Update the dictionary with the key/value pairs from other,
        overwriting existing keys.

        `update()` accepts either another dictionary object or an iterable of
        key/value pairs (as tuples or other iterables of length two). 
        If keyword arguments are specified, the dictionary is then updated with 
        those key/value pairs: `d.update(red=1, blue=2)`.
        
        Returns:
            None: No return
        """
        return self.__dict__.update(*args, **kwargs)

    def values(self):
        """ Return a list of the dictionary’s values.

        In Python 3.x `dict.values()` returns a view object, while in Python 2.x it returns a list.

        Returns:
            list: _description_
        """
        return self.__dict__.values()

class _DictTestCase(_unittest.TestCase):
    # ----------> Initialization <----------
    def test_init_empty(self):
        d = dict()
        self.assertEqual(d, {})
        
    def test_init_kwargs(self):
        d = dict(a=1, b=2)
        self.assertEqual(d, {"a": 1, "b": 2})
        
    def test_init_dict(self):
        d = dict({"a": 1, "b": 2})
        self.assertEqual(d, {"a": 1, "b": 2})
        
    def test_init_dict_empty(self):
        d = dict({})
        self.assertEqual(d, {})
        
    def test_init_list_lists(self):
        d = dict([["a", 1], ["b", 2]])
        self.assertEqual(d, {"a": 1, "b": 2})
        
    def test_init_tuple_tuples(self):
        d = dict((("a", 1), ("b", 2)))
        self.assertEqual(d, {"a": 1, "b": 2})
        
    def test_init_list_tuples(self):
        d = dict([("a", 1), ("b", 2)])
        self.assertEqual(d, {"a": 1, "b": 2})
        

    # ----------> String conversions <----------
    def test_str(self):
        self.assertEqual(str(dict(first=1, second=2)), "{'first': 1, 'second': 2}")

    def test_repr(self):
        self.assertEqual(repr(dict(first=1, second=2)), "{'first': 1, 'second': 2}")

    def test_type(self):
        self.assertEqual(type(dict()).__name__, type({}).__name__)


    # ----------> Values get & set <----------
    def test_get(self):
        d = dict(first=1, second=2)
        self.assertEqual(d.get("first"), 1)
        self.assertEqual(d.get("second"), 2)
        self.assertEqual(d["first"], 1)
        self.assertEqual(d["second"], 2)
        self.assertRaises(KeyError, lambda: d["third"])
        self.assertEqual(d.get("third", None), None)

    def test_set(self):
        d = dict()
        d["first"] = 1
        d["second"] = 2
        self.assertEqual(d, {"first": 1, "second": 2})
    

    # ----------> Dictionary methods <----------
    def test_clear(self):
        d = dict(first=1, second=2)
        d.clear()
        self.assertEqual(d, {})
    
    def test_copy(self):
        d = dict(first=1, second=2)
        d2 = d.copy()
        self.assertEqual(d, d2)
        self.assertIsNot(d, d2)

    def test_fromkeys(self):
        d = dict.fromkeys(["first", "second"])
        self.assertEqual(d, {"first": None, "second": None})
        d = dict.fromkeys(["first", "second"], 1)
        self.assertEqual(d, {"first": 1, "second": 1})

    def test_items(self):
        d = dict(first=1, second=2)
        self.assertEqual(list(d.items()), [("first", 1), ("second", 2)])

    def test_keys(self):
        d = dict(first=1, second=2)
        self.assertEqual(list(d.keys()), ["first", "second"])

    def test_pop(self):
        d = dict(first=1, second=2)
        self.assertEqual(d.pop("first"), 1)
        self.assertEqual(d, {"second": 2})
        self.assertEqual(d.pop("third", None), None)
    
    def test_popitem(self):
        d = dict(first=1, second=2)
        self.assertEqual(d.popitem(), ("second", 2))
        self.assertEqual(d, {"first": 1})
    
    def test_setdefault(self):
        d = dict(first=1, second=2)
        self.assertEqual(d.setdefault("first"), 1)
        self.assertEqual(d.setdefault("third"), None)
        self.assertEqual(d, {"first": 1, "second": 2, "third": None})
    
    def test_update(self):
        d = dict(first=1, second=2)
        d.update({"third": 3})
        self.assertEqual(d, {"first": 1, "second": 2, "third": 3})
        d.update({"first": 3})
        self.assertEqual(d, {"first": 3, "second": 2, "third": 3})
        d.update({"first": 1, "second": 2, "third": 3})
        self.assertEqual(d, {"first": 1, "second": 2, "third": 3})
        d.update(first=3)
        self.assertEqual(d, {"first": 3, "second": 2, "third": 3})
        d.update(first=1, second=2, third=3)
        self.assertEqual(d, {"first": 1, "second": 2, "third": 3})
        d.update([("first", 3)])
        self.assertEqual(d, {"first": 3, "second": 2, "third": 3})
        d.update([("first", 1), ("second", 2), ("third", 3)])
        self.assertEqual(d, {"first": 1, "second": 2, "third": 3})
        d.update((("first", 3),))
        self.assertEqual(d, {"first": 3, "second": 2, "third": 3})
        d.update((("first", 1), ("second", 2), ("third", 3)))
        self.assertEqual(d, {"first": 1, "second": 2, "third": 3})

    def test_values(self):
        d = dict(first=1, second=2)
        self.assertEqual(list(d.values()), [1, 2])
    
    def test_list(self):
        d = dict(first=1, second=2)
        self.assertEqual(list(d), ["first", "second"])

    def test_len(self):
        d = dict(first=1, second=2)
        self.assertEqual(len(d), 2)
    
    def test_in(self):
        d = dict(first=1, second=2)
        self.assertEqual("first" in d.keys(), 1 == 1)
        self.assertEqual("first" in d, 1 == 1)
    
    def test_not_in(self):
        d = dict(first=1, second=2)
        self.assertEqual("dummy" not in d.keys(), 1 == 1)
        self.assertEqual("dummy" not in d, 1 == 1)
    
    def test_del(self):
        d = dict(first=1, second=2)
        del d["first"]
        self.assertEqual(d, {"second": 2})
    

    # ----------> Exceptions <----------
    def test_exception_arg_string(self):
        self.assertRaises(ValueError, lambda: dict("string"))

    def test_exception_init_arg_too_many(self):
        self.assertRaises(TypeError, lambda: dict("a", "b"))

        try:
            dict("a", "b")
        except:
            message = _sys.exc_info()[1]
            self.assertEqual(
                str(message),
                r"dict expected at most 1 argument, got 2",
            )

    def test_exception_init_tuple_syntax(self):
        # Single tuple MUST end with a comma
        self.assertRaises(ValueError, lambda: dict( ([1,2]) ))
        self.assertEqual(dict( ([1,2], ) ), {1:2})


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
