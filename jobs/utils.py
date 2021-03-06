import json, os
from typing import Dict
from pyspark.sql.dataframe import DataFrame

def json_from_value(key, value):
    return json.dumps({key: value})

def json_from_df(key, dataframe: DataFrame):
    return json.dumps({key: df_to_json(dataframe)}, indent = 4)

def json_from_dict(dict: Dict):
    for key in dict:
        dict[key] = df_to_json(dict[key])
    
    return json.dumps(dict, indent = 4)

def df_to_json(dataframe: DataFrame):
    return dataframe.toJSON().map(lambda j: json.loads(j)).collect()

def write_to_file(json_string, filepath):
    if not os.path.exists('spark-outputs'):
        os.mkdir('spark-outputs')

    with open(filepath, 'w') as f:
        f.write(json_string)
