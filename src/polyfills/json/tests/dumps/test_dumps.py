import unittest

import polyfills.json as json

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
            str(3.14e10), # With '31400000000.0' tests failed on Python 2.2 and lower
            "Exponential numbers should work"
        )

    def test_bool(self):
        # Python >2.5 ==> `True` is defined as an actual boolean object
        if str(1==1) == 'True':
            self.assertEqual(
                json.dumps(1 == 1),
                "true"
            )
            self.assertEqual(
                json.dumps(1 == 0),
                "false"
            )
        
        # Python 2.2 - 2.3  ==> `True` is defined as `1`
        # Python < 2.2      ==> `True` is NOT defined, so the polyfill is needed
        elif str(1==1) == '1':
            self.assertEqual(
                json.dumps(1 == 1),
                "1"
            )
            self.assertEqual(
                json.dumps(1 == 0),
                "0"
            )
        
            if IS_POLYFILL_AVAILABLE:
                self.assertEqual(
                    json.dumps(_bool.bool(1)),
                    "true"
                )
                self.assertEqual(
                    json.dumps(_bool.bool(0)),
                    "false"
                )
            else:
                raise Exception("Polyfill is not available! Test is not complete.")
        else:
            raise Exception("Unexpected boolean value: %s" % str(1==1))

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

    def test_conversion_keys(self):
        self.assertEqual(
            json.dumps({True: 1}),
            '{"true": 1}',
        )
        self.assertEqual(
            json.dumps({False: 0}),
            '{"false": 0}',
        )
        self.assertEqual(
            json.dumps({None: None}),
            '{"null": null}',
        )
        self.assertEqual(
            json.dumps({1: 1}),
            '{"1": 1}',
        )
        self.assertEqual(
            json.dumps({1.1: 1.1}),
            '{"1.1": 1.1}',
        )
    
    def test_quotes(self):
        """ Quotes should be escaped (see #15) """
        self.assertEqual(
            json.dumps({"\"": "\""}),
            r'{"\"": "\""}',
            "Double quotes should be escaped both in keys and values"
        )
        self.assertEqual(
            json.dumps({"'": "'"}),
            r"""{"'": "'"}""",
            "Single quotes should be kept as-is",
        )

    
    def test_escape(self):
        self.assertEqual(
            json.dumps({"key": "va'lue"}),
            r"""{"key": "va'lue"}""",
            "Single quotes do not need to be escaped"
        )
        self.assertEqual(
            json.dumps({'k"ey': 'va"lue'}),
            r"""{"k\"ey": "va\"lue"}""",
            "Double quotes should be escaped"
        )
        self.assertEqual(
            json.dumps({r"k\ey": r"va\lue"}),
            r"""{"k\\ey": "va\\lue"}""",
            "Backslashes should be escaped both in keys and values"
        )

    def test_complex(self):
        if str(1==1) == 'True':
            __true__ = 1==1
        elif str(1==1) == '1':
            if IS_POLYFILL_AVAILABLE:
                __true__ = _bool.bool(1)
            else:
                raise Exception("Polyfill is not available! Test is not complete.")
        else:
            raise Exception("Unexpected boolean value: %s" % str(1==1))
        
        dump = json.dumps({
            "string": "value",
            "string_too": "2",
            "boolean": __true__,
            "integer": 14,
            "float": 27.3,
            "null": None,
        })
        assert '"string": "value"' in dump
        assert '"string_too": "2"' in dump
        assert '"boolean": true' in dump
        assert '"integer": 14' in dump
        assert '"float": 27.3' in dump
        assert '"null": null' in dump


if __name__ == '__main__':
    unittest.main(verbosity=2)