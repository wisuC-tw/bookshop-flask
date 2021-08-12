from pyspark.sql import SparkSession
import aggregated_views
import price_analytics
import rating_mean
import logging
import json
import utils as U

APP_NAME = "Bookshop spark jobs"

if __name__ == '__main__':
    
    spark = SparkSession.builder.appName(APP_NAME).getOrCreate()

    books3000 = spark.read.options(header='True', inferSchema='True') \
                                .csv("data/books-3000.csv")
    books3000.show(5)

    mean_value = rating_mean.find_mean(books3000)
    highly_rated = rating_mean.highly_rated(books3000, mean_value)
    less_rated = rating_mean.less_rated(books3000, mean_value)
    
    sum = price_analytics.total_cost_all_books(books3000)
    books_in_price_range = price_analytics.books_in_price_range(books3000, min=1000, max=2000)

    year_to_books_dict = aggregated_views.aggregate_by_year(books3000)
    books_by_one_year = aggregated_views.aggregate_by_one_year(books3000, year=2015)
    author_to_books_dict = aggregated_views.aggregate_by_author(books3000)
    books_by_one_author = aggregated_views.aggregate_by_one_author(books3000, author="Stephenie Meyer")

    print(U.json_from_value("mean", mean_value))
    print(U.json_from_df("highly_rated", highly_rated))
    print(U.json_from_df("less_rated", less_rated))
    
    print(U.json_from_value("sum", round(sum, 2)))
    print(U.json_from_df("books", books_in_price_range))

    print(U.json_from_dict(year_to_books_dict))
    print(U.json_from_df("2015", books_by_one_year))
    print(U.json_from_dict(author_to_books_dict))
    print(U.json_from_df("Stephenie Meyer", books_by_one_author))

    
    spark.stop() 
