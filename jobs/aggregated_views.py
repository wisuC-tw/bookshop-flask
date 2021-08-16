from pyspark.sql import DataFrame
import jobs.utils as utils

def aggregate_by_year(books3000: DataFrame, year=None):
    return aggregate(books3000, year, 'original_publication_year')

def aggregate_by_author(books3000: DataFrame, author=None):
    return aggregate(books3000, author, 'author')

def aggregate(books3000: DataFrame, key, col_name: str):
    if key:
        keys = [key]
    else:
        keys = sorted([x[col_name] for x in books3000.select(col_name).distinct().collect() if x[col_name]])
    key_to_books_dict = {str(key):None for key in keys}
    for key in keys:
        temp = books3000.filter(books3000[col_name] == key)
        key_to_books_dict[str(key)] = temp
    
    return key_to_books_dict

def run(books3000: DataFrame):
    year_to_books_dict = aggregate_by_year(books3000)
    books_by_one_year = aggregate_by_year(books3000, year=2015)
    author_to_books_dict = aggregate_by_author(books3000)
    books_by_one_author = aggregate_by_author(books3000, author="Stephenie Meyer")

    utils.write_to_file(utils.json_from_dict(year_to_books_dict), 'spark-outputs/year.json')
    utils.write_to_file(utils.json_from_dict(books_by_one_year), 'spark-outputs/year_single.json')
    utils.write_to_file(utils.json_from_dict(author_to_books_dict), 'spark-outputs/author.json')
    utils.write_to_file(utils.json_from_dict(books_by_one_author), 'spark-outputs/author_single.json')
