# Standard library imports
import datetime
import logging

# Third party imports
import pandas as pd
from pandas.api.types import is_numeric_dtype, is_string_dtype

# Reader imports
from assetutilities.common.data import ReadData
from assetutilities.common.update_deep import update_deep_dictionary
from assetutilities.common.utilities import is_file_valid_func

read_data = ReadData()

df_statistics_columns = [
    "column",
    "data_type",
    "min",
    "max",
    "mean",
    "stdev",
    "start_value",
    "end_value",
    "row_count",
    "no_of_unique_values",
    "row_count_per_unique_values",
    "unique_values",
]


class DataExploration:
    def __init__(self) -> None:
        pass

    def router(self, cfg):
        logging.info(f"Starting {cfg['basename']} application ...")

        cfg = self.get_cfg_with_master_data(cfg)

        df_array = self.get_df_data(cfg)
        
        df_statistics_summary = []
        for df in df_array:
            df_statistics = self.get_df_statistics(df)
            for column in df_statistics_columns:
                df_statistics_summary.append(df_statistics[column].tolist())

    def get_df_data(self, cfg):

        df_array = []
        for group_cfg in cfg["data"]["groups"]:
            analysis_root_folder = cfg["Analysis"]["analysis_root_folder"]
            file_is_valid, valid_file = is_file_valid_func(
                group_cfg["file_name"], analysis_root_folder
            )
            if not file_is_valid:
                raise ValueError(f'Invalid file name/path: {group_cfg["file_name"]}')

            df = pd.read_csv(valid_file)
            df = self.get_filtered_df(group_cfg, df)
            df_array.append(df)

        return df_array

    def get_inferred_df_data_types(self, df):
        df_columns = list(df.columns)
        df_column_data_types = []
        for column in df_columns:
            print(f"Data type for '{column}' : {type(df[column].iloc[0])}")
            print(f"First element for '{column}': {df[column].iloc[0]}")

            column_data_type = None
            if is_numeric_dtype(df[column]):
                column_data_type = "numeric"

            if is_string_dtype(df[column]):
                column_data_type = "string"

            if column_data_type == "string":
                try:
                    abc = pd.to_datetime(df[column].iloc[0])
                    column_data_type = "datetime"
                except:
                    pass

            if isinstance(df[column].iloc[0], datetime.datetime) or isinstance(
                df[column].iloc[0], datetime.date
            ):
                column_data_type = "datetime"

            df_column_data_types.append(column_data_type)
            print(f"Data type array is :{df_column_data_types}")

        return df_column_data_types

    def get_df_statistics(self, df):
        df_statistics = pd.DataFrame(columns=df_statistics_columns)
        df_column_data_types = self.get_inferred_df_data_types(df)
        df_columns = list(df.columns)
        column_index = 0
        for column in df_columns:
            df_column = column
            data_type = df_column_data_types[column_index]
            row_count = len(df)
            if data_type == "datetime":
                df[column] = pd.to_datetime(df[column])

            if data_type in ['numeric', 'datetime']:
                df_col_min = df[column].min()
                df_col_max = df[column].max()
                df_col_mean = df[column].mean()
                df_col_stdev = df[column].std()
            else:
                df_col_min = None
                df_col_max = None
                df_col_mean = None
                df_col_stdev = None

            unique_values = df[column].unique()
            no_of_unique_values = len(unique_values)
            row_count_per_unique_values = row_count / no_of_unique_values

            if no_of_unique_values > 20:
                unique_values = None
            else:
                unique_values = str(unique_values)

            df_col_start_value = df[column].iloc[0]
            df_col_end_value = df[column].iloc[-1]

            output_row = [
                df_column,
                data_type,
                df_col_min,
                df_col_max,
                df_col_mean,
                df_col_stdev,
                df_col_start_value,
                df_col_end_value,
                row_count,
                no_of_unique_values,
                row_count_per_unique_values,
                unique_values,
            ]
            df_statistics.loc[len(df_statistics)] = output_row

            column_index = column_index + 1

        return df_statistics



    def get_cfg_with_master_data(self, cfg):
        if "master_settings" in cfg:
            master_settings = cfg["master_settings"].copy()
            data_settings = cfg["data"]

            for group_index in range(0, len(data_settings["groups"])):
                group = data_settings["groups"][group_index].copy()
                group = update_deep_dictionary(master_settings["groups"], group)
                data_settings["groups"][group_index] = group.copy()

        return cfg


    def get_filtered_df(self, data_set_cfg, df):
        df = df.copy()
        if data_set_cfg.__contains__("filter"):
            df = read_data.df_filter_by_column_values(data_set_cfg.copy(), df)
        return df.copy()
