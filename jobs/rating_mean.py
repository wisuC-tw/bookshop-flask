from pyspark.sql import DataFrame
import jobs.utils as utils

def find_mean(books3000: DataFrame) -> int:
    mean = books3000
    mean = mean.agg({'average_rating': 'mean'})
    mean_value = mean.collect()[0][0]
    return mean_value    

def find_highly_rated(books3000: DataFrame, mean_value: int) -> DataFrame:
    highly_rated = books3000.filter((books3000['average_rating'] > mean_value))
    return highly_rated

def find_less_rated(books3000: DataFrame, mean_value: int) -> DataFrame:
    less_rated = books3000.filter((books3000['average_rating'] < mean_value))
    return less_rated

def run(books3000: DataFrame):
    mean_value = find_mean(books3000)
    highly_rated = find_highly_rated(books3000, mean_value)
    less_rated = find_less_rated(books3000, mean_value)

    print(utils.json_from_value("mean", mean_value))
    print(utils.json_from_df("highly_rated", highly_rated))
    print(utils.json_from_df("less_rated", less_rated))
