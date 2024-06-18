# Standard library imports
import datetime

# Third party imports
import pandas as pd
from pandas.api.types import is_numeric_dtype, is_string_dtype


class DataExploration:
    def __init__(self):
        pass

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


if __name__ == "__main__":

    # Define a dictionary containing employee data
    data = {
        "Name": ["Jai", "Princi", "Gaurav", "Anuj"],
        "Age": [27, 24, 22, 32],
        "Address": ["Delhi", "Kanpur", "Allahabad", "Kannauj"],
        "service_date": ["2020-01-20", "2020-02-23", "2021-03-24", "2022-01-05"],
    }

    # Convert the dictionary into DataFrame
    df = pd.DataFrame(data)
    print(df)

    data_dictionary = {"query": "", "csv_filename": "df_statistics.csv"}

    data_expl = DataExploration()
    df_statistics = data_expl.get_df_statistics(df)
    df_statistics.to_csv(data_dictionary["csv_filename"])
