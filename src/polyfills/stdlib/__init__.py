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
    item_type = type(__iterable).__name__
    iterables = (
        "list", "org.python.core.PyList", 
        "dict", "org.python.core.PyDictionary", 
        "tuple", "org.python.core.PyTuple"
    )

    if item_type in ["list", "org.python.core.PyList"]:
        elements = [ elem for elem in __iterable ]    # Make a copy of the original iterable
        elements.sort()

        value = []
        for element in elements:
            if type(element).__name__ in iterables:
                value.append(sorted(element))
            else:
                value.append(element)

        return value
    
    # ---> Dictionary
    #
    #      When passed a dictionary, the original `sorted` function
    #      sorts only its keys.
    elif item_type in ["dict", "org.python.core.PyDictionary"]:
        return sorted([ value for value in __iterable.keys()])
    
    elif item_type in ["tuple", "org.python.core.PyTuple"]:
        return sorted([ value for value in __iterable ])
    
    # ---> String
    #
    #      When passed a string, the original `sorted` function
    #      sorts its characters.
    elif item_type in ["str", "org.python.core.PyString"]:
        return sorted([ char  for char  in __iterable ])
    
    else:
        raise Exception("Unhandled type '%s' for iterable '%s'" % (item_type, __iterable))

