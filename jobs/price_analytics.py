from pyspark.sql import DataFrame
import jobs.utils as utils

def find_total_cost_all_books(books3000: DataFrame) -> int:
    sum = books3000 \
        .select((books3000['price'] * books3000['books_count']).alias("total")) \
        .agg({'total': 'sum'}).first()['sum(total)']
    return sum

def find_books_in_price_range(books3000: DataFrame, min: int, max: int) -> DataFrame:
    books_in_price_range = books3000.filter((books3000['price'] >= min) &
                                            (books3000['price'] <= max))
    return books_in_price_range

def run(books3000: DataFrame):
    sum = find_total_cost_all_books(books3000)
    books_in_price_range = find_books_in_price_range(books3000, min=1000, max=2000)

    utils.write_to_file(utils.json_from_value("sum", round(sum, 2)), 'spark-outputs/sum.json')
    utils.write_to_file(utils.json_from_df("books", books_in_price_range), 'spark-outputs/books_in_price_range.json')
