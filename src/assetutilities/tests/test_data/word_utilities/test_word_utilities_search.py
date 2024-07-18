"""
Not worked as intended. Difficult to work between Excel workbooks to keep live links.
Easier to just do a brute force copy and paste and rerun script if needed.
"""

# Standard library imports
import os
import sys
import pytest


# Third party imports

# Reader imports
from assetutilities.engine import engine


@pytest.mark.skip(reason="Only works in local drive")
def run_word_utilties_search_string(input_file, expected_result={}):
    if input_file is not None and not os.path.isfile(input_file):
        input_file = os.path.join(os.path.dirname(__file__), input_file)
    cfg = engine(input_file)

    # obtained_result = cfg[cfg['basename']]['properties']
    # expected_result = expected_result[cfg['basename']]['properties'].copy()

    # assert not deepdiff.DeepDiff(obtained_result,
    #                              expected_result,
    #                              ignore_order=True,
    #                              significant_digits=4)


@pytest.mark.skip(reason="Only works in local drive")
def get_valid_pytest_output_file(pytest_output_file):
    if pytest_output_file is not None and not os.path.isfile(pytest_output_file):
        pytest_output_file = os.path.join(os.path.dirname(__file__), pytest_output_file)
    return pytest_output_file


@pytest.mark.skip(reason="Only works in local drive")
def test_word_utilties_search_string():
    # input_file = 'src/assetutlities/tests/test_data/word_utilities/word_utilities.yml'
    input_file = "word_utilities.yml"

    # pytest_output_file = '../test_data/6d_buoy/buoy_6d_circular_px_0_pytest.yml'
    # pytest_output_file = get_valid_pytest_output_file(pytest_output_file)
    expected_result = {}
    # expected_result = ymlInput(pytest_output_file, updateYml=None)

    if len(sys.argv) > 1:
        sys.argv.pop()

    run_word_utilties_search_string(input_file, expected_result)


test_word_utilties_search_string()
