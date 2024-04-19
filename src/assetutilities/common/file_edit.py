import os
import itertools
import shutil
from assetutilities.common.utilities import is_file_valid_func

class FileEdit:

    def __init__(self) -> None:
        pass

    def router(self, cfg):
        if cfg['edit_type'] == 'concatenate':
            self.concatenate_files(cfg)

    def concatenate_files(self, cfg):
        if cfg['concatenate_type'] == 'array':
            self.concatenate_files_array(cfg)
        elif cfg['concatenate_type'] == '2d_array':
            self.concatenate_files_2d_array(cfg)

    def concatenate_files_array(self, cfg):
        for input_set in cfg['input']:
            input_files = input_set['input_files']
            output_filename = input_set['output_filename']

            output_dir = input_set.get('output_dir', None)
            if output_dir is None:
                output_dir = cfg['Analysis']['analysis_root_folder']
            output_filename_path = os.path.join(output_dir, output_filename)

        cfg = self.concatenate_one_set(cfg, input_files, output_filename_path)
        return cfg

    def concatenate_one_set(self, cfg, input_files, output_filename_path):
        analysis_root_folder = cfg['Analysis']['analysis_root_folder']
        with open(output_filename_path,'wb') as wfd:
            for f in input_files:
                file_is_valid, valid_file = is_file_valid_func(f,
                                                        analysis_root_folder)

                with open(valid_file,'rb') as fd:
                    shutil.copyfileobj(fd, wfd)

        return cfg

    def concatenate_files_2d_array(self, cfg):
        for input_set in cfg['input']:
            output_files = {'ext': [], 'no_ext': []}
            output_dir = input_set.get('output_dir', None)
            if output_dir is None:
                output_dir = cfg['Analysis']['analysis_root_folder']
            file_extension = input_set.get('file_extension', 'dat') 

            input_file_labels = input_set.get('input_file_labels')
            input_files_2d = input_set['input_files']


            input_files_2d_permutations = list(itertools.product(*input_files_2d))
            input_files_labels_permutations = list(itertools.product(*input_file_labels))

            for set_2d_idx in range(0, len(input_files_2d_permutations)):
                output_filename = input_set['output_basename']
                file_array = list(input_files_2d_permutations[set_2d_idx])
                label_array = list(input_files_labels_permutations[set_2d_idx])

                for label in label_array:
                    if label == '':
                        label_separator = ''
                    else:
                        label_separator = '_'
                    output_filename = output_filename + label_separator + label

                output_filename_path = os.path.join(output_dir, output_filename + '.' + file_extension)
                output_filename_path_no_ext = os.path.join(output_dir, output_filename)
                output_files['ext'].append(output_filename_path)
                output_files['no_ext'].append(output_filename_path_no_ext)

                cfg = self.concatenate_one_set(cfg, file_array, output_filename_path)

            self.prepare_custom_batch(input_set, output_files, cfg)

        return cfg

    def prepare_custom_batch(self, input_set, output_files, cfg):
        batch_cfg = input_set.get('batch', None)
        batch_filename = os.path.join(cfg['Analysis']['analysis_root_folder'], cfg['Analysis']['file_name'] + '.bat')
        if batch_cfg is not None and batch_cfg['flag']:
            with open(batch_filename, 'w') as the_file:
                if batch_cfg['extension']:
                    for output_file_name in output_files['ext']:
                        the_file.write(batch_cfg['content']  + ' ' + output_file_name + '\n')
                else:
                    for output_file_name in output_files['no_ext']:
                        the_file.write(batch_cfg['content']  + ' ' + output_file_name + '\n')


