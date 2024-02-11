import unittest

from utils.str_utils import *


class StrUtilsTests(unittest.TestCase):
    def test_flag_leading_zeros(self):
        """test flag_leading_zeros fn"""
        test_cases: list[dict[str, any]] = [
            {'args': {'x': '1'}, 'returns': 0},
            {'args': {'x': '01'}, 'returns': 1},
            {'args': {'x': '001'}, 'returns': 1},
        ]

        # test return equals expected
        for case in test_cases:
            result = flag_leading_zeros(**case['args'])
            expected_result = case['returns']
            self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
