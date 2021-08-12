from pyspark.sql import DataFrame

def total_cost_all_books(books3000: DataFrame) -> int:
    df1 = books3000.select(
        (books3000['price'] * books3000['books_count']).alias("total")
    )
    df1.show(5)
    df2 = df1.agg({'total': 'sum'})
    df2.show(5)
    sum = df2.collect()[0][0]
    return sum

def books_in_price_range(books3000: DataFrame, min: int, max: int) -> DataFrame:
    books_in_price_range = books3000.filter((books3000['price'] >= min) &
                                            (books3000['price'] <= max))
    books_in_price_range.show(5)
    return books_in_price_range
