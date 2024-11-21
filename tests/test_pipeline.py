#import os


def test_pass_pipeline():

    #library = 'assetutilities'
    root_directory = 'tests'
    summary_file = 'tests/yml_summary.txt'

    df = pd.read_csv(summary_file_pytest)

    with open(summary_file, 'r') as file:
        content = file.read()

    tests_passed = None
    for line in content.splitlines():
        if "Tests passed:" in line:
            tests_passed = int(line.split(":")[1].strip())
            break

    expected_result = 28

    #TODO 
    # https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.equals.html
    summary_file_pytest = 'tests/all_yml_status.csv'
    df_expected = pd.read_csv(summary_file_pytest)
    df.equals(df_expected)


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

