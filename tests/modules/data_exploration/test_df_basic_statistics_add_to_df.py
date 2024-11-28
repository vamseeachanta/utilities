# Standard library imports
import os
import sys

# Reader imports
from assetutilities.engine import engine
from assetutilities.common.yml_utilities import ymlInput
from assetutilities.modules.test_utilities.test_utilities import TestUtilities

tu = TestUtilities()

def run_process(input_file, expected_result={}) -> dict:
    if input_file is not None and not os.path.isfile(input_file):
        input_file = os.path.join(os.path.dirname(__file__), input_file)
    cfg = engine(input_file)
    assert True

    return cfg


def test_run_process() -> None:
    input_file = "df_basic_statistics_add_to_df.yml"

    pytest_output_file = "results/df_basic_statistics_add_to_df_pytest.yml"
    pytest_output_file = tu.get_valid_pytest_output_file(os.path.dirname(__file__), pytest_output_file)
    expected_result = ymlInput(pytest_output_file, updateYml=None)

    if len(sys.argv) > 1:
        sys.argv.pop()

    run_process(input_file, expected_result)




test_run_process()
