import unittest

from utils.float_utils import *


class FloatUtilsTests(unittest.TestCase):

    def test_flag_outlier(self):
        """test flag_outlier fn"""
        test_cases: list[dict[str, any]] = [
            {'args': {'x': 0.1, 'mean': 0.5, 'std': 0.1}, 'returns': 1},
            {'args': {'x': 0.9, 'mean': 0.5, 'std': 0.1}, 'returns': 1},
            {'args': {'x': 0.5, 'mean': 0.5, 'std': 0.1}, 'returns': 0},
            {'args': {'x': 0.4, 'mean': 0.5, 'std': 0.1}, 'returns': 0},
            {'args': {'x': 0.6, 'mean': 0.5, 'std': 0.1}, 'returns': 0},
        ]

        # test return equals expected
        for case in test_cases:
            result = flag_outlier(**case['args'])
            expected_result = case['returns']
            self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
