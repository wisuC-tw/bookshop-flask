from pyspark.sql import DataFrame

def aggregate_by_year(books3000: DataFrame):
    years = sorted([x['original_publication_year'] for x in books3000.select("original_publication_year").distinct().collect() if x['original_publication_year']])
    print(years)
    year_to_books_dict = {str(year):None for year in years}
    for year in years:
        temp = books3000.filter(books3000['original_publication_year'] == year)
        temp.show(2)
        year_to_books_dict[str(year)] = temp
    return year_to_books_dict

def aggregate_by_one_year(books3000: DataFrame, year: int) -> DataFrame:
    df2 = books3000.filter(books3000['original_publication_year'] == year)
    df2.show(5)
    return df2

def aggregate_by_author(books3000: DataFrame):
    authors = sorted([x['author'] for x in books3000.select("author").distinct().collect() if x['author']])
    print(authors)
    author_to_books_dict = {author:None for author in authors}
    for author in authors:
        temp = books3000.filter(books3000['author'] == author)
        temp.show(2)
        author_to_books_dict[author] = temp
    return author_to_books_dict

def aggregate_by_one_author(books3000: DataFrame, author: str) -> DataFrame:
    df4 = books3000.filter(books3000['author'] == author)
    df4.show(5)
    return df4