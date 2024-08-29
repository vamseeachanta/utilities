# Standard library imports
import os
import subprocess

# Third party imports
import pandas as pd
from colorama import Fore, Style
from colorama import init as colorama_init

colorama_init()

def run_yaml_files(root_directory):
    
    folders = []
    filenames = []
    statuses = []

    for root, dirs, files in os.walk(root_directory):
        
        # Skip files in the root directory
        if root == root_directory:
            continue
        
        for filename in files:

            if filename.endswith(('.yml', '.yaml')) and not filename.lower().startswith('app'):
                file_path = os.path.join(root, filename)
                try:
                    result = subprocess.run(['python', '-m', 'assetutilities', file_path], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    print(result.stdout.decode())
                    folders.append(os.path.relpath(root, root_directory))  
                    filenames.append(filename)
                    statuses.append('Success')
                except subprocess.CalledProcessError as e:
                    print(e.stderr.decode())  
                    folders.append(os.path.relpath(root, root_directory)) 
                    filenames.append(filename)
                    statuses.append('Failed')

        df = pd.DataFrame({'Folder': folders, 'Filename': filenames, 'Status': statuses})

        df = df.sort_values(by=['Status', 'Folder'], ascending=[False, True])

        output_csv = os.path.join(root_directory, 'file_status.csv')
        df.to_csv(output_csv, index=False)


    print(f'Detailed output: {df}')
    print(f'No. of files processed: {len(filenames)}')
    print(f"Tests passed: {Fore.GREEN}{len(df[df['Status'] == 'Success'])}{Style.RESET_ALL}")
    print(f"Tests Failed: {Fore.RED}{len(df[df['Status'] == 'Failed'])}{Style.RESET_ALL}")
    print('Done!')


if __name__ == '__main__':
    library = 'assetutilities'
    root_directory = f'src/{library}/tests/test_data'   
    run_yaml_files(root_directory)
