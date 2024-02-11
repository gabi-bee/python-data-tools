import unittest

from helpers.df_col_checks import *

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


class DfChecksTests(unittest.TestCase):
    _dict_to_df_examples = {
        'ex_inf_int1': {'int1': [0, 1]},
        'ex_str_int1': {'int1': ['0', '1']},
        'ex_str_int1_leading0s': {'int1': ['0', '01']},
        'ex_str_leading0s_examples': {
            'int1': ['0', '1', '01'],
            'int2': ['0', '1', '001'],
            'int3': ['0', '01', np.nan],
            'int4': ['0', '01', '01'],
            'int5': ['0', '1', '2'],
            'int6': ['1', '2', '3']
        },
    }
    dfs = {key: pd.DataFrame.from_dict(value) for key, value in _dict_to_df_examples.items()}

    # test main functions ----------------------------------------------------------------------------------------------
    def test_run_suite_df_col_checks(self):
        """test run_suite_of_df_col_checks fn"""

        test_cases: list[dict[str, any]] = [
            {'args': {'df_inferred': pd.DataFrame.from_dict({'col1': [0, 0], 'col2': [1, 1]}),
                      'df_str': pd.DataFrame.from_dict({'col1': ['0', '0'], 'col2': ['1', '1']})}, 'returns': None},
            {'args': {'df_inferred': self.dfs['ex_inf_int1'], 'df_str': self.dfs['ex_str_int1']}, 'returns': None},
            {'args': {'df_inferred': self.dfs['ex_str_int1'], 'df_str': self.dfs['ex_str_int1']}, 'returns': None},
            {'args': {'df_inferred': self.dfs['ex_inf_int1'], 'df_str': self.dfs['ex_str_int1_leading0s']},
             'returns': None},

        ]

        # test return equals expected
        for i, case in enumerate(test_cases):
            print(f'\n\ncase: {i}')
            print(f'\ndf_inferred: \n{case["args"]["df_inferred"]}')
            print(f'\ndf_str: \n{case["args"]["df_str"]}')
            result: pd.DataFrame = run_suite_of_df_col_checks(**case['args'])
            # expected_result = case['returns']
            print(f'\nresult: \n{result}')

    # test helper functions --------------------------------------------------------------------------------------------

    # test individual check functions ----------------------------------------------------------------------------------
    def test_check_int_leading_zeros(self):
        """test check_int_leading_zeros fn"""

        test_cases: list[dict[str, any]] = [
            {'args': {'df_str': self.dfs['ex_str_int1']}, 'returns': pd.Series(data={'int1': 0})},
            {'args': {'df_str': self.dfs['ex_str_int1_leading0s']}, 'returns': pd.Series(data={'int1': 1})},
            {'args': {'df_str': self.dfs['ex_str_leading0s_examples']},
             'returns': pd.Series(data={'int1': 1, 'int2': 1, 'int3': 1, 'int4': 2, 'int5': 0, 'int6': 0})},
        ]

        # test return equals expected
        for case in test_cases:
            result: pd.Series = check_int_leading_zeros(**case['args'])[0]
            expected_result = case['returns']

            self.assertTrue(result.astype(int).equals(expected_result))
            self.assertEqual(result.name, 'int_leading_zeros')


if __name__ == '__main__':
    unittest.main()
