import pytest


@pytest.mark.usefixtures('dbt_test_utils')
class TestDeriveColumnsMacro:

    def test_derive_columns_correctly_generates_sql_with_source_columns(self):
        model = 'test_derive_columns_with_source_columns'

        var_dict = {'source_model': 'raw_source', 'columns': {'SOURCE': "!STG_BOOKING", 'EFFECTIVE_FROM': 'LOADDATE'}}
        process_logs = self.dbt_test_utils.run_dbt_model(model=model, model_vars=var_dict)
        expected_sql = self.dbt_test_utils.retrieve_expected_sql(self.current_test_name)
        actual_sql = self.dbt_test_utils.retrieve_compiled_model(model)

        assert 'Done' in process_logs
        assert expected_sql == actual_sql

    def test_derive_columns_correctly_generates_sql_without_source_columns(self):
        model = 'test_derive_columns_without_source_columns'

        var_dict = {'columns': {'SOURCE': "!STG_BOOKING", 'LOADDATE': 'EFFECTIVE_FROM'}}
        process_logs = self.dbt_test_utils.run_dbt_model(model=model, model_vars=var_dict)
        actual_sql = self.dbt_test_utils.retrieve_compiled_model(model)
        expected_sql = self.dbt_test_utils.retrieve_expected_sql(self.current_test_name)

        assert 'Done' in process_logs
        assert expected_sql == actual_sql

    def test_derive_columns_correctly_generates_sql_with_only_source_columns(self):
        model = 'test_derive_columns_with_only_source_columns'

        var_dict = {'source_model': 'raw_source'}
        process_logs = self.dbt_test_utils.run_dbt_model(model=model, model_vars=var_dict)
        actual_sql = self.dbt_test_utils.retrieve_compiled_model(model)
        expected_sql = self.dbt_test_utils.retrieve_expected_sql(self.current_test_name)

        assert 'Done' in process_logs
        assert expected_sql == actual_sql
