import pytest
import sys
import os
import pandas as pd

current_dir = os.path.dirname(__file__)
asset_directory = os.path.abspath(os.path.join(current_dir, '../../'))
if asset_directory not in sys.path:
    sys.path.insert(0, asset_directory)

from src.assetutilities.tests.test_data.test_all_yml import run_yaml_files

def test_pass_pipeline():

    root_directory = os.path.join(current_dir, 'test_data')
    
    run_yaml_files(root_directory)
    
    df = pd.read_csv('src\assetutilities\tests\test_data\file_status.csv')
    
    expected_result = 30
    
    assert len(df[df['Status'] == 'Success']) == expected_result
    



