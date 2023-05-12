import unittest

import polyfills.json as json

class BaseTestCase(unittest.TestCase):
    def test_string(self):
        self.assertEqual(
			json.loads('"string"'),
        	"string",
            "Strings should work"
		)
        
    def test_null(self):
        self.assertEqual(
			json.loads('null'),
        	None,
            "Null object should work"
		)
        
    def test_numbers(self):
        self.assertEqual(
			json.loads('157'),
        	157,
            "Integer numbers should work"
		)
        self.assertEqual(
			json.loads('3.14'),
        	3.14,
            "Floating point numbers should work"
		)
        self.assertEqual(
			json.loads('3.14e10'),
        	3.14e10,
            "Exponential numbers should work"
		)

    def test_bool(self):
        self.assertEqual(
			json.loads('true'),
        	1 == 1
		)
        self.assertEqual(
			json.loads('false'),
        	1 == 0
		)

    def test_custom_bool(self):
        self.assertEqual(
			json.loads('true', truthy_value="__TEST_TRUE__", falsy_value="__TEST_FALSE__"),
        	"__TEST_TRUE__"
		)
        self.assertEqual(
			json.loads('false', truthy_value="__TEST_TRUE__", falsy_value="__TEST_FALSE__"),
        	"__TEST_FALSE__"
		)

class ArrayTestCase(unittest.TestCase):       
    def test_array(self):
        self.assertEqual(
			json.loads('["value", 1, true, null]'),
        	["value", 1, True, None]
		)

    def test_array_nested(self):
        self.assertEqual(
			json.loads('["value", 1, [true, null]]'),
        	["value", 1, [True, None]]
		)
    

    def test_array_types(self):
        self.assertEqual(
			json.loads('["value", 1, [true, null], {"test": false}]'),
        	["value", 1, [True, None], {"test": False}]
		)
    

    def test_array_objects(self):
        self.assertEqual(
			json.loads('[{"key": true}, {"key": "Second"}, {"key": 3}, {"key": 4e1}]'),
        	[{"key": True}, {"key": "Second"}, {"key": 3}, {"key": 4e1}]
		)
    

    def test_array_with_spaces(self):
        self.assertEqual(
			json.loads('["value", 1, [true, "String with \\"quotes\\"\\n around"], {"test": false}, null]'),
        	["value", 1, [True, "String with \"quotes\"\n around"], {"test": False}, None]
		)
    

class ObjectTestCase(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(
            json.loads('{"string": "value", "key2": 1, "last": true}'),
            {"string": "value", "key2": 1, "last": True},
        )

    def test_nested_dict(self):
        self.assertEqual(
            json.loads('{"string": "value","dict": {"nested_key": "nested_value","test": true} }'),
            {"string": "value","dict": {"nested_key": "nested_value","test": True} },
        )

    def test_nested_dict_array(self):
        self.assertEqual(
			json.loads('{"string": "value","dict": {"nested_key": "nested_value","test": true}, "last": [1, 2, 3]}'),
        	{"string": "value","dict": {"nested_key": "nested_value","test": True}, "last": [1, 2, 3]}
		)
    

    def test_advanced(self):
        self.assertEqual(
			json.loads('{"string": "value","dict": {"nested_key": "nested_value","test": true}, "last": 1}'),
        	{"string": "value","dict": {"nested_key": "nested_value","test": True}, "last": 1}
		)
    

if __name__ == '__main__':
    unittest.main(verbosity=2)