from pyspark.sql import DataFrame

def find_mean(books3000: DataFrame) -> int:
    mean = books3000
    mean = mean.agg({'average_rating': 'mean'})
    mean.show()
    mean_value = mean.collect()[0][0]
    return mean_value    

def highly_rated(books3000: DataFrame, mean_value: int) -> DataFrame:
    highly_rated = books3000.filter((books3000['average_rating'] > mean_value))
    highly_rated.show(5)
    return highly_rated

def less_rated(books3000: DataFrame, mean_value: int) -> DataFrame:
    less_rated = books3000.filter((books3000['average_rating'] < mean_value))
    less_rated.show(5)
    return less_rated