#import os


def test_pass_pipeline():

    #library = 'assetutilities'
    root_directory = 'tests'
    summary_file = 'tests/yml_summary.txt'


    with open(summary_file, 'r') as file:
        content = file.read()

    tests_passed = None
    for line in content.splitlines():
        if "Tests passed:" in line:
            tests_passed = int(line.split(":")[1].strip())
            break

    expected_result = 28


    summary_file_pytest = 'tests/yml_summary_pytest.txt'

    with open(summary_file_pytest, 'r') as file:
        content = file.read()

    tests_passed = None
    for line in content.splitlines():
        if "Tests passed:" in line:
            expected_result = int(line.split(":")[1].strip())
            break

    # expected_result = 28

    assert tests_passed == expected_result

test_pass_pipeline()

