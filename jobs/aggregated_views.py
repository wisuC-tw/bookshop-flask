from pyspark.sql import DataFrame
import jobs.utils as utils

def aggregate_by_year(books3000: DataFrame):
    years = sorted([x['original_publication_year'] for x in books3000.select("original_publication_year").distinct().collect() if x['original_publication_year']])
    year_to_books_dict = {str(year):None for year in years}
    for year in years:
        temp = books3000.filter(books3000['original_publication_year'] == year)
        year_to_books_dict[str(year)] = temp
    return year_to_books_dict

def aggregate_by_one_year(books3000: DataFrame, year: int) -> DataFrame:
    df2 = books3000.filter(books3000['original_publication_year'] == year)
    return df2

def aggregate_by_author(books3000: DataFrame):
    authors = sorted([x['author'] for x in books3000.select("author").distinct().collect() if x['author']])
    author_to_books_dict = {author:None for author in authors}
    for author in authors:
        temp = books3000.filter(books3000['author'] == author)
        author_to_books_dict[author] = temp
    return author_to_books_dict

def aggregate_by_one_author(books3000: DataFrame, author: str) -> DataFrame:
    df4 = books3000.filter(books3000['author'] == author)
    return df4

def run(books3000: DataFrame):
    year_to_books_dict = aggregate_by_year(books3000)
    books_by_one_year = aggregate_by_one_year(books3000, year=2015)
    author_to_books_dict = aggregate_by_author(books3000)
    books_by_one_author = aggregate_by_one_author(books3000, author="Stephenie Meyer")

    print(utils.json_from_dict(year_to_books_dict))
    print(utils.json_from_df("2015", books_by_one_year))
    print(utils.json_from_dict(author_to_books_dict))
    print(utils.json_from_df("Stephenie Meyer", books_by_one_author))
