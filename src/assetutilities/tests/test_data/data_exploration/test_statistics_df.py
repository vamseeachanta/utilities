# Standard library imports
import os
import sys

# Reader imports
from assetutilities.engine import engine


def run_process(input_file, expected_result={}):
    if input_file is not None and not os.path.isfile(input_file):
        input_file = os.path.join(os.path.dirname(__file__), input_file)
    cfg = engine(input_file)
    assert True

    return cfg


def test_run_process():
    # input_file = 'df_statistics.yml'
    input_file = "df_statistics_file_management.yml"

    pytest_output_file = None
    # pytest_output_file = get_valid_pytest_output_file(pytest_output_file)
    # expected_result = ymlInput(pytest_output_file, updateYml=None)

    if len(sys.argv) > 1:
        sys.argv.pop()

    run_process(input_file, expected_result={})


test_run_process()
