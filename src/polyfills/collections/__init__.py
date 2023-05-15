""" Provides backport of some of the `collections` features. """

class OrderedDict:
    """ Drop-in replacement for the Python 2.7 OrderedDict class. """
    def __init__(self, d={}, **data):
        self._keys = []
        self._values = [] # type: list

        if(type(d).__name__ not in ["dict", "org.python.core.PyDictionary"]):    # Fix for Jython types
            raise TypeError("the dictionary entered is not valid - either regular dictionary or OrderedDictionary object is expected")
        
        for key in d.keys():
            self[key] = d[key]  # In the ord-dict add an entry at the key 'key' and give the value at 'key' in d 

        if data:
            for key in data:
                self[key] = data[key]

    # ---------------------
    # Overwrite `__getitem__`, `__setitem__`, `__delitem__` so that 
    # `dict[key] = value` correctly sets `self._keys` and `self._values`.
    def __getitem__(self, key):
        if key not in self._keys:
            raise KeyError("The key %s isn't in the dictionary" % key)

        index = self._keys.index(key)
        return self._values[index]

    def __setitem__(self, key, value):
        if key in self._keys:
            ind = self._keys.index(key)
            self._values[ind] = value
        else:
            self._keys.append(key)
            self._values.append(value)

    def __delitem__(self, key):
        if key not in self._keys:
            raise KeyError("The key %s isn't in the dictionary" % key)
        else:
            ind = self._keys.index(key)
            del self._keys[ind]
            del self._values[ind]
    # ---------------------

    """
    Functions `repr` and `str` return the same results:

    >>> d = collections.OrderedDict({"test":True})
    >>> repr(d)
    "OrderedDict([('test', True)])"
    >>> str(d)
    "OrderedDict([('test', True)])"
    """
    def __repr__(self):
        string = "OrderedDict({"
        first_time = 1 == 1    # Fix for Python < 2.3
        for key, value in self.items():
            if not first_time:
                string += ", " # Add comma to separate entries
            else:
                first_time = 1 == 0
            string += repr(key) + ": " + repr(value)
        string += "})"
        return string
    
    def __str__(self):
        return repr(self)
    # ---------------------

    def __len__(self):
        return len(self._keys)

    def __contains__(self, key):
        return key in self._keys
    
    def __eq__(self, other):
        true = 1 == 1     # Fix for Python v. < 2.3
        false = 1 == 0    # Fix for Python v. < 2.3

        # if isinstance(other, OrderedDict):
        #     print("Comparing the same object...")
        # else: 
        #     print("Comparing two different objects...")

        if len(self) != len(other):
            return false
        for p, q in  zip(self.items(), other.items()):
            if p != q:
                return false
        return true
    
    def __ne__(self, other):
        return not self == other

    def __iter__(self):
        return iter(self._keys)

    # ---> Methods
    def items(self):
        items = []
        for i in range(len(self._keys)):
            key = self._keys[i]
            val = self._values[i]
            items.append((key, val))
        return items

    def keys(self):
        return list(self._keys)

    def values(self):
        return list(self._values)
    
    def clear(self):
        self._keys = []
        self._values = []
        return None
    
    def get(self, key, default):
        if key not in self._keys:
            raise KeyError("The key %s isn't in the dictionary" % key)

        index = self._keys.index(key)
        return self._values[index]

    def copy(self):
        new_dict = OrderedDict()
        for key,value in self.items():
            new_dict[key] = value
        return new_dict