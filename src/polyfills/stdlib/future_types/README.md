# Future types

This module contains types that will be part of the standard library in newer versions (`>2.3`).

Currently 2 types are supported:

- [`bool`](bool.py) (which became available from Python 2.3)
- [`dict`](dict.py)

## Boolean values

The [`bool`](bool.py) module provides boolean values (**`True`** and **`False`**) for those Python versions that do not support them.

### Features

The `bool` module provides:

- **`True`** and **`False`**:

    ```python
    wsadmin>works = True
    wsadmin>works
    True
    wsadmin>if works: print("Works!")
    ...
    Works!
    wsadmin>works == True
    1
    wsadmin>works is True
    1
    wsadmin>works is not False
    1
    wsadmin>True == (1 == 1)
    1
    ```

- a `bool` class to **cast** expressions and values to `True` or `False`:

    ```python
    wsadmin>import os
    wsadmin>is_win = bool(os.name == "nt")
    wsadmin>is_win
    False
    wsadmin>bool([])
    False
    wsadmin>bool(["not-empty"])
    True
    ```

    It can also be used to check the **type** of a variable:

    ```python
    wsadmin>isinstance(is_win, bool)
    1
    wsadmin>isinstance(True, bool)
    1
    wsadmin>isinstance("True", bool)
    0
    wsadmin>isinstance(1, bool)
    0
    ```

### History

This is what happens when you try to set a variable to a boolean value in Jython <= 2.2.

```python
wsadmin>my_var = True
WASX7015E: Exception running command: "my_const = True"; exception information:
com.ibm.bsf.BSFException: exception from Jython:
Traceback (innermost last):
  File "<input>", line 1, in ?
NameError: True

wsadmin>
```

#### Workarounds

##### Workaround #1

A possible solution would be to **manually set `True` and `False`** to the result of a _boolean operation_:

```python
wsadmin>True, False = (1==1), (1==0)
```

This _works in the shell_, but if used in a modern **IDE** it will warn you about some **`SintaxError`** (which are not ignorable via `# type: ignore`).

##### Workaround #2

We can _fix that_ by defining the variables using **`exec`** so that the IDE does not complain:

```python
wsadmin>exec("try: (True, False)\nexcept NameError: exec('True = 1==1; False = 1==0')")
```

##### Testing workarounds

Either way we are left with `True` and `False` and that may seem ok:

```python
wsadmin>True
1
wsadmin>False
0
wsadmin>my_var = True
wsadmin>if my_var:
wsadmin>        print("Works")
wsadmin>
Works
wsadmin>if my_var == True:
wsadmin>        print("Works")
wsadmin>
Works
wsadmin>if my_var is True:
wsadmin>        print("Works")
wsadmin>
Works
```

The **problems** arise when we try to guess whether the value is actually a **boolean or an integer**...

Look at the following example:

```python
wsadmin>my_var
1
wsadmin>
wsadmin>type(my_var) == type(2)
1
wsadmin>
wsadmin>type(my_var).__name__
'org.python.core.PyInteger'
```

Is `my_var` a **boolean** or an **integer**? Since there is no actual `bool` type, there is no way to know!

#### Solution

The `bool` module comes to the rescue!  

By including it in our shell/script we are able to use `True` and `False` as if they were native objects (_almost_).  

##### Testing solution

Now let's run the same tests we ran [before](#testing-workarounds).

```python
wsadmin>True
True
wsadmin>False
False
wsadmin>my_var = True
wsadmin>if my_var:
wsadmin>        print("Works")
wsadmin>
Works
wsadmin>if my_var == True:
wsadmin>        print("Works")
wsadmin>
Works
wsadmin>if my_var is True:
wsadmin>        print("Works")
wsadmin>
Works
```

Is the problem we addressed before still there?

```python
wsadmin>my_var
True
wsadmin>
wsadmin>type(my_var) == type(2)
0
wsadmin>
wsadmin>type(my_var).__name__
'org.python.core.PyInstance'
wsadmin>
```

As you can see we can safely assume that the value is **NOT an integer**. To know whether the variable is a boolean value or not we just have to check if is an instance of the `bool` class (provided in the `bool` module):

```python
wsadmin>my_var = True
wsadmin>isinstance(my_var, bool)
1
wsadmin>my_var2 = 1
wsadmin>isinstance(my_var2, bool)
0
```
