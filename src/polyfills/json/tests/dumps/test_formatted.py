import unittest

import polyfills.json as json

class ParametersTestCase(unittest.TestCase):
    def test_positional_arguments (self):
        self.assertEqual(
            json.dumps([ 1, 2, 3 ], 4),
            '[\n    1, \n    2, \n    3\n]',
        )
    def test_keyword_arguments (self):
        self.assertEqual(
            json.dumps([ 1, 2, 3 ], indent=4),
            '[\n    1, \n    2, \n    3\n]',
        )
        

if __name__ == '__main__':
    unittest.main(verbosity=2)