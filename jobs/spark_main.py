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

    rating_mean.run(books3000)
    price_analytics.run(books3000)
    aggregated_views.run(books3000)
    
    spark.stop() 
