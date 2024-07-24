# Standard library imports
import os

# Third party imports
import pandas as pd


    
    folders = []
    filenames = []
    statuses = []

    for subfolder in subfolders:
        subfolder_path = os.path.join(root_directory, subfolder)
        if os.path.exists(subfolder_path) and os.path.isdir(subfolder_path):
            
            for filename in os.listdir(subfolder_path):
                if filename.endswith(('.yml', '.yaml')) and not filename.lower().startswith('app'):
                    file_path = os.path.join(subfolder_path, filename)
                    try:
                        result = subprocess.run(['python', '-m', library, file_path], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                        print(result.stdout.decode()) 
                        folders.append(subfolder)
                        filenames.append(filename)
                        statuses.append('Success')
                    except subprocess.CalledProcessError as e:
                        print(e.stderr.decode())  
                        folders.append(subfolder)
                        filenames.append(filename)
                        statuses.append('Failed')

            df = pd.DataFrame({'Folder': folders, 'Filename': filenames, 'Status': statuses})

            df.loc[df['Folder'].duplicated(), 'Folder'] = ''

            output_csv = os.path.join(root_directory, 'file_status.csv')
            df.to_csv(output_csv, index=False)

    print(f'Detailed output: {df}')
    print(f'No. of files processed: {len(filenames)}')
    print("Tests passed: ", len(df[df['Status'] == 'Success']))
    print("Tests failed: ", len(df[df['Status'] == 'Failed']))
    print('Done!')


if __name__ == '__main__':
    library = 'assetutilities'
    root_directory = f'src/{library}/tests/test_data' 
    subfolders = ['data_exploration','edit_pdf','excel_utilities','file_edit','file_management','read_pdf','visualization','word_utilities','yml']  
    run_yaml_files(root_directory, subfolders)
