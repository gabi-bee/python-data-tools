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

    def test_reshape_with_expected_cols(self):
        """test update_with_expected_cols fn"""

        test_cases: list[dict[str, any]] = [
            {'args': {'df': pd.DataFrame.from_dict({'c': [0]}), 'expected_cols': ['a', 'b', 'c']},
             'returns': pd.DataFrame.from_dict({'a': [np.nan], 'b': [np.nan], 'c': [0]})},

            {'args': {'df': pd.DataFrame.from_dict({'c': [0]}), 'expected_cols': ['a', 'b', 'c'], 'reshape': False},
             'returns': pd.DataFrame.from_dict({'c': [0], 'a': [np.nan], 'b': [np.nan]})},

            {'args': {'df': pd.DataFrame.from_dict({'c': [0], 'd': [0]}), 'expected_cols': ['a', 'b', 'c']},
             'returns': pd.DataFrame.from_dict({'a': [np.nan], 'b': [np.nan], 'c': [0], 'd': [0]})},

            {'args': {'df': pd.DataFrame.from_dict({'c': [0], 'd': [0]}),
                      'expected_cols': ['a', 'b', 'c'], 'reshape': False},
             'returns': pd.DataFrame.from_dict({'c': [0], 'd': [0], 'a': [np.nan], 'b': [np.nan]})},

            {'args': {'df': pd.DataFrame.from_dict({'c': [0], 'd': [0]}),
                      'expected_cols': ['a', 'b', 'c'], 'drop_unexpected': True},
             'returns': pd.DataFrame.from_dict({'a': [np.nan], 'b': [np.nan], 'c': [0]})},

            {'args': {'df': pd.DataFrame.from_dict({'c': [0], 'd': [0]}),
                      'expected_cols': ['a', 'b', 'c'], 'reshape': False, 'drop_unexpected': True},
             'returns': pd.DataFrame.from_dict({'c': [0], 'a': [np.nan], 'b': [np.nan]})},
        ]

        # test return equals expected
        for case in test_cases:
            result: pd.DataFrame = update_with_expected_cols(**case['args'])
            expected_result = case['returns']
            self.assertTrue(result.equals(expected_result))


if __name__ == '__main__':
    unittest.main()
