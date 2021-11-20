import json
import shutil
from pathlib import Path
import pandas as pd


def get_working_dir():
    return Path.cwd()


def clean_directory(directory_path):
    target = f'{get_working_dir()}/{directory_path}'

    try:
        shutil.rmtree(f'{target}')
        print(f'NICE: {target} cleaned.')
    except Exception as e:
        print(f'FAILED to remove: {target}')


def output_to_file(foldername, filename, result):
    '''
    Accepts a dictionary!!!
    '''
    directory = f'{get_working_dir()}/{foldername}'
    file_path = f'{directory}/{filename}.json'

    try:
        # Create directory if not exists
        Path(directory).mkdir(parents=True, exist_ok=True)

        # Write result to file
        with open(file_path, 'w') as f:
            json.dump(result, f, indent=4)
        print(f"NICE: {file_path} created.")
    except Exception as e:
        print(f'FAILED: creating {file_path}: {e}')


def filter_df(df, column_name, column_value):
    df = df[df[column_name] == column_value]
    return df


def filter_by_range(df, column_name, upper=None, lower=None):
    if upper is None and lower is None:
        return df
    elif upper is None:
        return df[df[column_name] >= lower]
    elif lower is None:
        return df[df[column_name] <= upper]
    else:
        internal = df[df[column_name] >= lower]
        return internal[internal[column_name] <= upper]


def calc_statistics(df, numeric_column_name):
    numeric_column = df[numeric_column_name]
    max = numeric_column.max()
    min = numeric_column.min()
    mean = numeric_column.mean()
    res = {'max': max, 'min': min, 'mean': mean}
    return res


def convert_df_to_dict(df):
    return df.to_dict('records')


def convert_dict_to_df(dict_list):
    return pd.DataFrame.from_dict(dict_list)


def generate_co2_spending_by_criteria(df, criteria_column):
    unique = df[criteria_column].unique()
    res = list()
    for u in unique:
        dict_item = {}
        dict_item['name'] = u
        filtered = filter_df(df, criteria_column, u)
        dict_item['TotalSpendEUR'] = filtered['SpendEUR'].sum()
        dict_item['TotalCo2Emission'] = filtered['co2_emission'].sum()
        res.append(dict_item)

    return convert_dict_to_df(res)
