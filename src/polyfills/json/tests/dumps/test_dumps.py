import unittest

import polyfills.json as json

class BaseTestCase(unittest.TestCase):
    def test_string(self):
        self.assertEqual(
            json.dumps("string"),
            '"string"',
            "Strings should work"
        )
        
    def test_null(self):
        self.assertEqual(
            json.dumps(None),
            'null',
            "Null object should work"
        )
        
    def test_numbers(self):
        self.assertEqual(
            json.dumps(157),
            '157',
            "Integer numbers should work"
        )
        self.assertEqual(
            json.dumps(3.14),
            '3.14',
            "Floating point numbers should work"
        )
        self.assertEqual(
            json.dumps(3.14e10),
            '31400000000.0',
            "Exponential numbers should work"
        )

    def test_bool(self):
        self.assertEqual(
            json.dumps(True),
            "true"
        )
        self.assertEqual(
            json.dumps(False),
            "false"
        )

    def test_custom_bool(self):
        self.assertEqual(
            json.dumps("__TEST_TRUE__", truthy_value="__TEST_TRUE__", falsy_value="__TEST_FALSE__"),
            'true'
        )
        self.assertEqual(
            json.dumps("__TEST_FALSE__", truthy_value="__TEST_TRUE__", falsy_value="__TEST_FALSE__"),
            'false'
        )


class ArrayTestCase(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(json.dumps([]), '[]')
    
    def test_simple(self):
        self.assertEqual(
            json.dumps(["", "test1", "", "test2", ""]),
            '["", "test1", "", "test2", ""]'
        )


class ObjectTestCase(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(json.dumps({}), '{}')
    
    def test_simple(self):
        self.assertEqual(
            json.dumps({"key": "value"}),
            '{"key": "value"}'
        )

    def test_complex(self):
        self.assertEqual(
            json.dumps({
                "string": "value",
            }), 
            '{"string": "value"}'
        )
        self.assertEqual(
            json.dumps({
                "string_too": "2",
            }), 
            '{"string_too": "2"}'
        )
        self.assertEqual(
            json.dumps({
                "boolean": True,
            }), 
            '{"boolean": true}'
        )
        self.assertEqual(
            json.dumps({
                "integer": 14,
            }), 
            '{"integer": 14}'
        )
        self.assertEqual(
            json.dumps({
                "float": 27.3,
            }), 
            '{"float": 27.3}'
        )
        self.assertEqual(
            json.dumps({
                "null": None,
            }), 
            '{"null": null}'
        )


if __name__ == '__main__':
    unittest.main(verbosity=2)