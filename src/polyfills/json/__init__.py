""" Basic implementation of a JSON parser written in pure Python for very old Python versions (2.2 and lower). """
import re as _re

IS_BOOLEAN_DEFINED = str(1==1) == 'True'
IS_POLYFILL_AVAILABLE = 0 == 1

if not IS_BOOLEAN_DEFINED:
    # Try to import the boolean polyfill
    try:
        import polyfills.stdlib.future_types.bool as _bool
        exec("True = _bool.bool(1); False = _bool.bool(0)")
        IS_POLYFILL_AVAILABLE = 1 == 1
    except ImportError:
        pass

__all__ = ["dumps", "dump", "loads", "load"]

# The following list of characters is taken from the builtin `json` module.
#
# I used a list instead of a dictionary because on Py<=3.5 dictionaries are
# unordered by default, which is a problem in this case since the backslash
# may be escaped multiple times.
ESCAPED_CHARS = [
    {"from": '\\', "to": '\\\\'},
    {"from": '"', "to": '\\"'},
    {"from": '\b', "to": '\\b'},
    {"from": '\f', "to": '\\f'},
    {"from": '\n', "to": '\\n'},
    {"from": '\r', "to": '\\r'},
    {"from": '\t', "to": '\\t'},
]


class BaseJSONError(Exception):
    """ Base exception for the JSON library. """

class JSONDecodeError(BaseJSONError):
    """ Thrown when there is an error while decoding a JSON String. """

def escape_string(string):
    # type: (str) -> str
    """Escapes a string so that it can be used as a JSON string.

    Args:
        string (str): The string to escape.

    Returns:
        str: The escaped string.
    """
    for special_char in ESCAPED_CHARS:
        string = string.replace(special_char["from"], special_char["to"])
    
    return string

def dumps(
        obj,
        indent=None,          # type: int|None
        truthy_value=None,
        falsy_value=None,
    ):
    """Transforms a Python dictionary into a valid json string.

    Args:
        obj (dict|list): The object (dictionary or list) that needs to be converted to a JSON string.
        indent (int, optional): The number of spaces to use as indentation. Defaults to None.
        numbers_as_boolean (int, optional): Wether to interpret `0` and `1` as boolean values. MUST be set for Python versions < 2.3. Defaults to 0.

    Returns:
        json (str): A string representation of a valid JSON object.
    """
    if not IS_BOOLEAN_DEFINED and not IS_POLYFILL_AVAILABLE and (truthy_value is None and falsy_value is None):
        raise Exception(
            "No boolean values (True/False) detected and the 'truthy_value' and 'falsy_value' options are not set." +
            " If you're using this module on Python < 2.3 set them accordingly."
        )

    if (truthy_value is None and falsy_value is not None) or (truthy_value is not None and falsy_value is None):
        raise Exception("The 'truthy_value' and 'falsy_value' options MUST be BOTH either set or unset.")

    obj_type = type(obj)
    obj_string_parts = []             # type: list[str]

    indent_spaces = 0                 # type: int
    needs_indentation = indent is not None and indent != "" and indent > 0    # type: bool
    
    if needs_indentation:
        indent_spaces = indent    # type: ignore


    #  ---> Handle JSON objects
    if obj_type == type({}):
        obj_string_parts.append("{")

        for key in obj.keys(): # pyright: ignore[reportGeneralTypeIssues]
            if len(obj_string_parts) > 1:
                obj_string_parts[-1] += ", "
            value = dumps(obj[key], indent_spaces, truthy_value, falsy_value)
            parsed_key = dumps(key)
            
            # Remove quotes from the parsed key, because we will add them
            #   manually later.
            if parsed_key.startswith('"') and parsed_key.endswith('"'):
                parsed_key = parsed_key[1:-1]

            obj_string_parts.append('"%s": %s' % (
                parsed_key,
                str(value),
            ))
        
        obj_string_parts.append("}")
    #endif
    

    #  ---> Handle JSON arrays
    elif obj_type in [type([None,]), type((None,))]:
        obj_string_parts.append("[")
        for item in obj:
            if len(obj_string_parts) > 1:
                obj_string_parts[-1] += ", "
            obj_string_parts.append(dumps(item, indent_spaces, truthy_value, falsy_value))

        obj_string_parts.append("]")
    #endif


    # ---> Handle and encode other JSON types:
    #   >>> json.dumps("True")
    #   '"True"'
    #
    #   >>> json.dumps(True)
    #   'true'
    #
    #   >>> json.dumps(2, indent=4)
    #   '2'
    #
    #   >>> json.dumps(None)
    #   'null'
    #
    # ------------------------------------------------------
    #
    # Extra parameters for Jython v. < 2.3:
    #   >>> json.dumps("True", truthy_value="True", falsy_value="False")
    #   'true'
    #
    #   >>> json.dumps(0, truthy_value=1, falsy_value=0)
    #   'false'
    #
    else:
        # ---> Boolean types
        if truthy_value is not None and obj == truthy_value:
            return "true"
        elif falsy_value is not None and obj == falsy_value:
            return "false"
        elif obj_type != type("") and str(obj) == "True":
            return "true"
        elif obj_type != type("") and str(obj) == "False":
            return "false"

        # ---> Base types
        elif obj_type == type(""):
            return '"%s"' % escape_string(str(obj))
        elif obj_type == type(5):
            return str(obj)
        elif obj_type == type(5.0):
            return str(obj)
        
        # ---> Null type
        elif obj_type == type(None):
            return "null"
    #endif

    if needs_indentation:
        # Indent every line (except the the first and last lines - the
        #   boundaries of the JSON object) by {indent} spaces if needed (check
        #   `needs_indentation` for the constraints).
        for index in range(1, len(obj_string_parts)-1):
            obj_string_parts[index] = '\n'.join([ 
                " " * indent_spaces + string 
                for string in obj_string_parts[index].splitlines()
            ])
            

        return '\n'.join(obj_string_parts)
    #endif

    return ''.join(obj_string_parts)


def loads(
        json_str, # type: str
        truthy_value=None,
        falsy_value=None,
    ):
    """
    Parses a JSON string and returns the corresponding Python object.

    Args:
        json_str (str): A JSON string.
        truthy_value (bool, optional): The value to use for boolean `true`. Defaults to None.
        falsy_value (bool, optional): The value to use for boolean `false`. Defaults to None.

    Returns:
        Any: A Python object corresponding to the JSON string.
    """
    json_str = json_str.strip()

    if not IS_BOOLEAN_DEFINED and not IS_POLYFILL_AVAILABLE and (truthy_value is None and falsy_value is None):
        print(
            "Warning: No boolean values (True/False) detected and the 'truthy_value' and 'falsy_value' options are not set." +
            " If you're using this module on Python < 2.3 set them accordingly."
        )

    if (truthy_value is None and falsy_value is not None) or (truthy_value is not None and falsy_value is None):
        raise Exception("The 'truthy_value' and 'falsy_value' options MUST be BOTH either set or unset.")


    # Ensure that the input is a string.
    if type(json_str) != type(""):
        raise TypeError('Expected a string, got %s' % type(json_str))

    # Define temporary boolean values for old Jython versions (<2.3) that do not support True/False
    __false__ = 1 == 0  # type: bool
    __true__ = 1 == 1   # type: bool

    is_inside_string = __false__  # type: bool

    last_string = ()    # type: tuple[int, ...]
    last_key = ()       # type: tuple[int, ...]
    last_value = ()     # type: tuple[int, ...]

    nesting_levels = [] # type: list[int]

    result = None # type: None | dict | list

    # ---> Decode JSON object
    if json_str.startswith("{"):
        for index in range(len(json_str)):
            char = json_str[index]

            # ----> JSON strings
            #
            #       Note that keys MUST be strings enclosed in double quotes.
            if char == '"' and json_str[index-1] != "\\":
                # Parse strings only in the main level
                if len(nesting_levels) > 1:
                    continue

                is_inside_string = not is_inside_string
                if is_inside_string:
                    last_string = (index,)

                    # ---> Strings can be both values and keys
                    if len(last_key) < 2:
                        last_key = (index+1,)
                    
                    # Leave the string quoted `"`, so that the value will be decoded as a string
                    elif len(last_value) < 2:
                        last_value = (index,)
                else:
                    if not last_string:
                        raise Exception("Did not expect to find 'last_string' empty")
                    
                    # ---> Strings can be both values and keys
                    if len(last_key) < 2:
                        last_key += (index,)
                    
                    # Leave the string quoted `"`, so that the value will be decoded as a string
                    elif len(last_value) < 2:
                        last_value += (index+1,)
                
                continue
            # endif

            # Skip spaces or characters in a string
            if char.isspace() or is_inside_string:
                continue

                
            # Check for characters not allowed by JSON standard (outside of strings)
            if char == "'":
                raise JSONDecodeError("Single quote is not permitted by JSON standard")

            # --------------------------------------------------------------


            if char in ["{", "["]:
                if result is not None and len(nesting_levels) == 0:
                    raise JSONDecodeError("You are trying to redefine an existing object! Maye you forgot a comma (',')?")
                    
                nesting_levels.append(index)
                continue

            elif char in ["}", "]"]:
                last_bracket = nesting_levels.pop()

                # Support for empty objects
                if len(last_key) == 0 and len(nesting_levels) == 0:
                    result = {}
                    continue

                if len(last_key) != 2:
                    raise JSONDecodeError("Malformed JSON input: Object key was not properly closed")
                
                key_name = json_str[last_key[0]:last_key[1]]

                # Nested JSON object (will be processed when either a comma or a
                # closing curly brace are found)
                #
                #  Example closing curly brace: 
                #       ..., "object": {"nested": "value"}} 
                #
                #  Example comma: 
                #       ..., "object": {"nested": "value"}, "key": true}
                #
                if len(nesting_levels) == 1 and len(last_value) == 0:
                    last_value = (last_bracket, index+1)
                    continue

                # If the previous was the last JSON property (not a string) in the object, add its index
                #
                #  Example: ..., "key": true}
                if len(last_value) == 1:
                    last_value += (index,)

                # Initialize the result if not done already
                if result is None:
                    result = {}


                # If something is still in the value buffer then add it to the object.
                # This is the case, for example, when a non-object value is last.
                if len(nesting_levels) == 0 and len(last_value) == 2:
                    key_value = json_str[last_value[0]:last_value[1]]
                    result[key_name] = loads(key_value, truthy_value, falsy_value)
                    
                    last_key = ()
                    last_value = ()
                    
                continue

            # --------------------------------------------------------------
            

            # ----> Skip content of deeper levels
            #      
            #       The nested values will be recursively parsed 
            #       every time their parent object closes.
            if len(nesting_levels) > 1:
                continue
            
            
            # ----> End of key
            elif char == ":":
                if len(last_key) != 2:
                    raise JSONDecodeError("Malformed JSON input: Object key cannot be empty")
                
                continue
            
            # ----> End of value
            elif char == ",":
                if len(last_key) != 2:
                    raise JSONDecodeError("Comma was found but with no preceding value: %s" % str(last_key))
                if len(last_value) == 0 or len(last_value) > 2:
                    raise JSONDecodeError("Malformed JSON input: Object value was not properly closed")
                
                # Values have only the starting index when are neither strings,
                # objects or arrays (i.e. bool, int or null).
                if len(last_value) == 1:
                    last_value += (index,)

                # Initialize the result if not done already
                if result is None:
                    result = {}

                
                key_name = json_str[last_key[0]:last_key[1]]
                value = json_str[last_value[0]:last_value[1]]

                # Parse the JSON value
                result[key_name] = loads(value, truthy_value, falsy_value)

                last_key = ()
                last_value = ()
            # endif

            # ----> Raw value (ex. integer, float, boolean, null)
            #
            #       Save the found index and process the value after
            #       the comma or when the closing bracket is found.
            else:
                if not last_value:
                    last_value = last_value + (index,)
            # endif
                
    # ---> Decode JSON array
    elif json_str.startswith("["):
        for index in range(len(json_str)):
            char = json_str[index]

            # ----> JSON strings
            #
            #       Note that keys MUST be strings enclosed in double quotes.
            if char == '"' and json_str[index-1] != "\\":
                # Parse strings only in the main level
                if len(nesting_levels) > 1:
                    continue

                is_inside_string = not is_inside_string
                if is_inside_string:
                    # Leave the string quoted `"`, so that the value will be decoded as a string
                    if len(last_value) < 2:
                        last_value = (index,)
                else:
                    # Leave the string quoted `"`, so that the value will be decoded as a string
                    if len(last_value) < 2:
                        last_value += (index+1,)
                
                continue
            # endif

            # Skip spaces or characters in a string
            if char.isspace() or is_inside_string:
                continue

                
            # Check for characters not allowed by JSON standard (outside of strings)
            if char == "'":
                raise JSONDecodeError("Single quote is not permitted by JSON standard")

            # --------------------------------------------------------------


            # ----> JSON Object/Array
            if char in ["{", "["]:
                if result is not None and len(nesting_levels) == 0:
                    raise JSONDecodeError("You are trying to redefine an existing object! Maye you forgot a comma (',')?")
                    
                nesting_levels.append(index)
                continue

            elif char in ["}", "]"]:
                last_bracket = nesting_levels.pop()
                
                # Nested JSON object (will be processed when either a comma or a
                # closing curly brace are found)
                #
                #  Example closing curly brace: 
                #       ..., "value", [true, null]]
                #
                #  Example comma: 
                #       ..., "object": {"nested": "value"}, "key": true}
                #
                if len(nesting_levels) == 1 and len(last_value) == 0:
                    last_value = (last_bracket, index+1)
                    continue


                # If the previous was the last JSON property (not a string) in the object, add its index
                #
                #  Example: ..., "key": true}
                if len(last_value) == 1:
                    last_value += (index,)

                # Initialize the result if not done already
                if result is None:
                    result = []

                # If something is still in the value buffer then add it to the object.
                # This is the case, for example, when a non-object value is last.
                if len(nesting_levels) == 0 and len(last_value) == 2:
                    key_value = json_str[last_value[0]:last_value[1]]
                    result.append(loads(key_value, truthy_value, falsy_value))
                    
                    last_value = ()
                continue
            
            
            # --------------------------------------------------------------
            

            # ----> Skip content of deeper levels
            #      
            #       The nested values will be recursively parsed 
            #       every time their parent object closes.
            if len(nesting_levels) > 1:
                continue
            
            
            # ----> Wrong syntax
            elif char == ":":
                raise JSONDecodeError("Unexpected character '%s' inside array" % char)
            
            # ----> End of value
            elif char == ",":
                if len(last_value) == 0 or len(last_value) > 2:
                    raise JSONDecodeError("Malformed JSON input: Array value was not properly closed")
                
                # Values have only the starting index when are neither strings,
                # objects or arrays (i.e. bool, int or null).
                if len(last_value) == 1:
                    last_value += (index,)

                # Initialize the result if not done already
                if result is None:
                    result = []

                
                value = json_str[last_value[0]:last_value[1]]

                # Parse the JSON value
                result.append(loads(value, truthy_value, falsy_value))

                last_value = ()
            # endif

            # ----> Raw value (ex. integer, float, boolean, null)
            #
            #       Save the found index and process the value after
            #       the comma or when the closing bracket is found.
            else:
                if not last_value:
                    last_value = last_value + (index,)
            # endif
                


    # ---> Decode JSON value
    else:
        # https://stackoverflow.com/a/66379646/8965861
        REGEX_FLOAT   = _re.compile(r"(?i)^\s*[+-]?(?:inf(inity)?|nan|(?:\d+\.?\d*|\.\d+)(?:e[+-]?\d+)?)\s*$")
        REGEX_INTEGER = _re.compile(r"^([+-]?[1-9]\d*|0)$")

        # ---> String
        #
        #      TODO: Convert unicode strings to character and viceversa
        if json_str.startswith('"') and json_str.endswith('"'):
            result = str(json_str[1:-1]) \
                .replace('\\"', '"') \
                .replace('\\\\', '\\') \
                .replace('\\/', '/') \
                .replace('\\b', '\b') \
                .replace('\\f', '\f') \
                .replace('\\n', '\n') \
                .replace('\\r', '\r') \
                .replace('\\t', '\t') \
                .replace('\\\\u', '\\u')
        
        # ---> Numbers
        elif REGEX_INTEGER.match(json_str):
            result = int(json_str)
        
        elif REGEX_FLOAT.match(json_str):
            result = float(json_str)
        
        # ---> Boolean
        elif json_str == "true":
            if truthy_value is not None:
                result = truthy_value
            elif IS_POLYFILL_AVAILABLE:
                return _bool.bool(1)
            else:
                result = __true__
            
        elif json_str == "false":
            if falsy_value is not None:
                result = falsy_value
            elif IS_POLYFILL_AVAILABLE:
                result = _bool.bool(0)
            else:
                result = __false__
        
        # ---> Null
        elif json_str == "null":
            result = None
        
        else:
            raise JSONDecodeError("Unhandled json value: %s" % json_str)
        
    if is_inside_string or nesting_levels:
        raise JSONDecodeError("Malformed JSON input")

    return result


def load(
        fh,
        truthy_value=None, 
        falsy_value=None
    ):
    """ Deserialize fp (a `.read()`-supporting text file or binary file containing a JSON document) to a Python object.
    
    Args:
        fh (file): A File-like object.
        truthy_value (bool, optional): The value to use for boolean `true`. Defaults to None.
        falsy_value (bool, optional): The value to use for boolean `false`. Defaults to None.

    Returns:
        Any: The deserialized Python object.
    """
    return loads(fh.read(), truthy_value, falsy_value)
    

def dump(
        fh,
        obj,
        indent=None,          # type: int|None
        truthy_value=None,
        falsy_value=None
    ):
    fh.write(dumps(
        obj,
        indent,
        truthy_value,
        falsy_value,
    ))
    