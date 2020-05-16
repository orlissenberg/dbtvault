import pytest


@pytest.mark.usefixtures('dbt_test_utils')
class TestHashColumnsMacro:

    def test_hash_columns_correctly_generates_hashed_columns_for_single_columns(self):
        model = 'test_hash_columns'

        var_dict = {
            'columns': {
                'BOOKING_PK': 'BOOKING_REF', 'CUSTOMER_PK': 'CUSTOMER_ID'}}
        process_logs = self.dbt_test_utils.run_dbt_model(model=model, model_vars=var_dict)
        actual_sql = self.dbt_test_utils.retrieve_compiled_model(model)
        expected_sql = self.dbt_test_utils.retrieve_expected_sql(self.current_test_name)

        assert 'Done' in process_logs
        assert expected_sql == actual_sql

    def test_hash_columns_correctly_generates_hashed_columns_for_composite_columns(self):
        model = 'test_hash_columns'

        var_dict = {
            'columns': {
                'BOOKING_PK': 'BOOKING_REF', 'CUSTOMER_DETAILS': ['ADDRESS', 'PHONE', 'NAME']}}
        process_logs = self.dbt_test_utils.run_dbt_model(model=model, model_vars=var_dict)
        actual_sql = self.dbt_test_utils.retrieve_compiled_model(model)
        expected_sql = self.dbt_test_utils.retrieve_expected_sql(self.current_test_name)

        assert 'Done' in process_logs
        assert expected_sql == actual_sql

    def test_hash_columns_correctly_generates_sorted_hashed_columns_for_composite_columns(self):
        model = 'test_hash_columns'

        var_dict = {
            'columns': {
                'BOOKING_PK': 'BOOKING_REF', 'CUSTOMER_DETAILS': {
                    'columns': ['ADDRESS', 'PHONE', 'NAME'], 'sort': True}}}

        process_logs = self.dbt_test_utils.run_dbt_model(model=model, model_vars=var_dict)
        actual_sql = self.dbt_test_utils.retrieve_compiled_model(model)
        expected_sql = self.dbt_test_utils.retrieve_expected_sql(self.current_test_name)

        assert 'Done' in process_logs
        assert expected_sql == actual_sql

    def test_hash_columns_correctly_generates_sorted_hashed_columns_for_multiple_composite_columns(self):
        model = 'test_hash_columns'

        var_dict = {
            'columns': {
                'BOOKING_PK'      : 'BOOKING_REF',
                'CUSTOMER_DETAILS': {'columns': ['ADDRESS', 'PHONE', 'NAME'], 'sort': True},
                'ORDER_DETAILS'   : {'columns': ['ORDER_DATE', 'ORDER_AMOUNT'], 'sort': False}}}

        process_logs = self.dbt_test_utils.run_dbt_model(model=model, model_vars=var_dict)
        actual_sql = self.dbt_test_utils.retrieve_compiled_model(model)
        expected_sql = self.dbt_test_utils.retrieve_expected_sql(self.current_test_name)

        assert 'Done' in process_logs
        assert expected_sql == actual_sql

    def test_hash_columns_correctly_generates_unsorted_hashed_columns_for_composite_columns_mapping(self):
        model = 'test_hash_columns'

        var_dict = {
            'columns': {
                'BOOKING_PK': 'BOOKING_REF', 'CUSTOMER_DETAILS': {
                    'columns': ['ADDRESS', 'PHONE', 'NAME']}}, }

        process_logs = self.dbt_test_utils.run_dbt_model(model=model, model_vars=var_dict)
        actual_sql = self.dbt_test_utils.retrieve_compiled_model(model)
        expected_sql = self.dbt_test_utils.retrieve_expected_sql(self.current_test_name)

        assert 'Done' in process_logs
        assert expected_sql == actual_sql

    def test_hash_columns_correctly_generates_sql_from_yaml(self):
        model = 'test_hash_columns'

        process_logs = self.dbt_test_utils.run_dbt_model(model=model)
        expected_sql = self.dbt_test_utils.retrieve_expected_sql(self.current_test_name)
        actual_sql = self.dbt_test_utils.retrieve_compiled_model(model)

        assert 'Done' in process_logs
        assert expected_sql == actual_sql

    def test_hash_columns_correctly_generates_sql_with_constants_from_yaml(self):
        model = 'test_hash_columns_with_constants'

        process_logs = self.dbt_test_utils.run_dbt_model(model=model)
        expected_sql = self.dbt_test_utils.retrieve_expected_sql(self.current_test_name)
        actual_sql = self.dbt_test_utils.retrieve_compiled_model(model)

        assert 'Done' in process_logs
        assert expected_sql == actual_sql

    def test_hash_columns_raises_warning_if_mapping_without_sort(self):
        model = 'test_hash_columns_missing_sort'
        
        process_logs = self.dbt_test_utils.run_dbt_model(model=model)
        expected_sql = self.dbt_test_utils.retrieve_expected_sql(self.current_test_name)
        actual_sql = self.dbt_test_utils.retrieve_compiled_model(model)
        warning_message = "You provided a list of columns under a 'column' key, " \
                          "but did not provide the 'sort' flag. HASHDIFF columns should be sorted."

        assert warning_message in process_logs
        assert expected_sql == actual_sql
