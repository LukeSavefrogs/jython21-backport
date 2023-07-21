""" A "quick-and-dirty" patch for boolean values in Python <2.3.

For more complex use cases, consider using the `bool` type from the `polyfills.stdlib.future_types`.

Usage:

```
import polyfills.stdlib.boolean

if True:
    print "Works"
```
"""

#! Jython 2.1 does not have boolean types (https://lukesavefrogs.github.io/wsadmin-type-hints/getting_started/tips-n-tricks/#workaround-for-jython-22-and-lower)
exec("try: (True, False)\nexcept NameError: exec('True = 1==1; False = 1==0')")
