import unittest

from utils.df_utils import *


class DfUtilsTests(unittest.TestCase):
    _dict_to_df_examples = {
        'ex_int1': {'int1': [0, 1]},
        'ex_str1': {'str1': ['0', '1']},

    }
    dfs = {key: pd.DataFrame.from_dict(value) for key, value in _dict_to_df_examples.items()}

    def test_get_dtype_cols_dict(self):
        """test get_dtype_cols_dict fn"""

        test_cases: list[dict[str, dict[str, any]] | dict[str, dict[str, list[str]]]] = [
            {'args': {'df': self.dfs['ex_int1']},
             'returns': {'int64': ['int1']}},

            {'args': {'df': self.dfs['ex_str1']},
             'returns': {'object': ['str1']}},

            {'args': {'df': self.dfs['ex_int1'], 'expected_keys': ['object']},
             'returns': {'int64': ['int1'], 'object': []}},

            {'args': {'df': self.dfs['ex_int1'], 'expected_keys': ['int64']},
             'returns': {'int64': ['int1']}},
        ]

        # test return equals expected
        for case in test_cases:
            self.assertDictEqual(get_dtype_cols_dict(**case['args']), case['returns'])


if __name__ == '__main__':
    unittest.main()
