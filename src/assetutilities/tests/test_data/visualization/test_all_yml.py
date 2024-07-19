# read all yml files in the current directory
# Loop through each yml file and run the below command
  # Hint1: python subprocess;  (Easier route). 
  # Hint2: subprocess separate command prompt. You have open a minconda prompt and ensure same python enviornment is used. to run each yml file
# If it ran, get success or failure. If one yml file fails.. then fail the test else the test passes
    # save a csv with all success and failures.

import os
import subprocess
import pandas as pd

def run_yaml_files(directory):
    # Initialize lists to store the results
    filenames = []
    statuses = []

    # Loop through all YAML files in the directory
    for filename in os.listdir(directory):
        if filename.endswith('.yml') or filename.endswith('.yaml'):
            file_path = os.path.join(directory, filename)
            try:
                # Run the command
                result = subprocess.run(['python', '-m', 'assetutilities', file_path], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                print(result.stdout.decode())  # Print the command output
                filenames.append(filename)
                statuses.append('Success')
            except subprocess.CalledProcessError as e:
                print(e.stderr.decode())  # Print the error output
                filenames.append(filename)
                statuses.append('Failed')

    # Create a DataFrame and save to CSV
    df = pd.DataFrame({'Filename': filenames, 'Status': statuses})
    output_csv = os.path.join(directory, 'results.csv')
    df.to_csv(output_csv, index=False)
    print(f'Results saved to {output_csv}')

# Usage example:
directory = r'src\assetutilities\tests\test_data\visualization'
run_yaml_files(directory)


