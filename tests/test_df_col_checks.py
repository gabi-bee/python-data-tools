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
        'ex_str_len_examples': {
            'str1': ['', '1', '12'],
            'str2': ['1', '1', np.nan],
            'str3': ['123456789', '123456789', np.nan],
        },
        'ex_all_dtype_examples': {
            'str1': ['a', 'b'],
            'str2': ['a', np.nan],
            'float1': [0.1, 1],
            'float2': [0.1, np.nan],
            'int1': [0, 1],
            'int2': [1, np.nan],
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

            # TODO add tests

    # test helper functions --------------------------------------------------------------------------------------------

    # test individual check functions ----------------------------------------------------------------------------------
    def test_check_all_dtypes(self):
        """test check_all_dtypes fn"""

        test_cases: list[dict[str, any]] = [
            {'args': {'df_inferred': self.dfs['ex_all_dtype_examples']},
             'returns': pd.Series(data={'str1': 'object', 'str2': 'object',
                                        'float1': 'float64', 'float2': 'float64',
                                        'int1': 'int64', 'int2': 'float64'  # int2 inferred as float64 due to np.nan
                                        })},
        ]

        # test return equals expected
        for case in test_cases:
            [result] = check_all_dtypes(**case['args'])  # single check in list
            expected_result = case['returns']

            self.assertTrue(result.equals(expected_result))
            self.assertEqual(result.name, 'dtype_py_inferred')

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
            [result] = check_int_leading_zeros(**case['args'])  # single check in list
            expected_result = case['returns']

            self.assertTrue(result.astype(int).equals(expected_result))
            self.assertEqual(result.name, 'int_leading_zeros')

    def test_check_str_len_min_max_checksum(self):
        """test check_str_len_min_max_checksum fn"""

        test_cases: list[dict[str, any]] = [
            {'args': {'df_str': self.dfs['ex_str_len_examples']},
             'returns': {
                 'min': pd.Series(data={'str1': 0, 'str2': 1, 'str3': 9}),  # min
                 'max': pd.Series(data={'str1': 2, 'str2': 1, 'str3': 9}),  # max
                 'sum': pd.Series(data={'str1': 3, 'str2': 2, 'str3': 18}),  # checksum
             }},
        ]

        # test return equals expected
        for case in test_cases:
            [str_len_min, str_len_max, str_len_checksum] = check_str_len_min_max_checksum(**case['args'])
            expected_results = case['returns']

            self.assertTrue(str_len_min.astype(int).equals(expected_results['min']))
            self.assertTrue(str_len_max.astype(int).equals(expected_results['max']))
            self.assertTrue(str_len_checksum.astype(int).equals(expected_results['sum']))
            self.assertEqual(str_len_min.name, 'str_len_min')
            self.assertEqual(str_len_max.name, 'str_len_max')
            self.assertEqual(str_len_checksum.name, 'str_len_checksum')


if __name__ == '__main__':
    unittest.main()
