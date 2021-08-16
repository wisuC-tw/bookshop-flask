from sparktestingbase.sqltestcase import SQLTestCase
from unittest.mock import patch
from jobs import aggregated_views, price_analytics, rating_mean, utils
import json

BASE_COLUMNS = [
    "id",
    "author",
    "title",
    "image_url",
    "small_image_url",
    "price",
    "books_count",
    "isbn",
    "isbn13",
    "original_publication_year",
    "original_title",
    "language_code",
    "average_rating"
]

ROW_1 = [
    1,
    "Johnny Johnson",
    "History Book",
    "https://www.a.com",
    "https://www.a.com",
    10000.0,
    7,
    316160202,
    9780316160210,
    2007,
    "Origins of Mankind",
    "en-US",
    3.68
]

ROW_2 = [
    2,
    "Al Rae",
    "Math Book",
    "https://www.b.com",
    "https://www.b.com",
    100.0,
    5,
    316130222,
    9730316460510,
    2017,
    "Origins of Multiverse",
    "en-US",
    4.63
]

ROW_3 = [
    3,
    "Johnny Johnson",
    "Economics Book",
    "https://www.c.com",
    "https://www.c.com",
    1000.0,
    3,
    816860282,
    2280886160880,
    2017,
    "How to be a billionaire",
    "en-US",
    1.32
]

ROW_4 = [
    4,
    "Quack Quack",
    "Duck Book",
    "https://www.d.com",
    "https://www.d.com",
    0.0,
    0,
    613860386,
    6270816140280,
    2007,
    "How to be a Duck",
    "en-US",
    3.21
]

SAMPLE_DATA = [
    ROW_1, ROW_2, ROW_3, ROW_4
]

SAMPLE_JSON = [
    {
        "id": 1,
        "author": "Johnny Johnson",
        "title": "History Book",
        "image_url": "https://www.a.com",
        "small_image_url": "https://www.a.com",
        "price": 10000.0,
        "books_count": 7,
        "isbn": 316160202,
        "isbn13": 9780316160210,
        "original_publication_year": 2007,
        "original_title": "Origins of Mankind",
        "language_code": "en-US",
        "average_rating": 3.68
    },
    {
        "id": 2,
        "author": "Al Rae",
        "title": "Math Book",
        "image_url": "https://www.b.com",
        "small_image_url": "https://www.b.com",
        "price": 100.0,
        "books_count": 5,
        "isbn": 316130222,
        "isbn13": 9730316460510,
        "original_publication_year": 2017,
        "original_title": "Origins of Multiverse",
        "language_code": "en-US",
        "average_rating": 4.63
    }
]

class SparkIntgrationTest(SQLTestCase):

    def test_should_return_mean_rating_value(self):
        input_dataframe = self.sqlCtx.createDataFrame(SAMPLE_DATA, BASE_COLUMNS)
        actual_value = rating_mean.find_mean(input_dataframe)
        self.assertAlmostEqual(3.21, actual_value)

    def test_should_return_list_of_books_above_mean_rating(self):
        input_dataframe = self.sqlCtx.createDataFrame(SAMPLE_DATA, BASE_COLUMNS)
        expected_df = self.sqlCtx.createDataFrame(
            [ROW_1, ROW_2],
            BASE_COLUMNS
        )
        actual_df = rating_mean.find_highly_rated(input_dataframe, 3.21)
        self.assertEqual(expected_df.schema, actual_df.schema)
        self.assertEqual(expected_df.collect(), actual_df.collect())
        self.assertDataFrameEqual(expected_df, actual_df)

    def test_should_return_list_of_books_below_mean_rating(self):
        input_dataframe = self.sqlCtx.createDataFrame(SAMPLE_DATA, BASE_COLUMNS)
        expected_df = self.sqlCtx.createDataFrame(
            [ROW_3],
            BASE_COLUMNS
        )
        actual_df = rating_mean.find_less_rated(input_dataframe, 3.21)
        self.assertEqual(expected_df.schema, actual_df.schema)
        self.assertEqual(expected_df.collect(), actual_df.collect())

    def test_should_return_sum_price_of_all_books(self):
        input_dataframe = self.sqlCtx.createDataFrame(SAMPLE_DATA, BASE_COLUMNS)
        actual_value = price_analytics.find_total_cost_all_books(input_dataframe)
        self.assertEqual(73500, actual_value)

    def test_should_return_books_in_given_price_range(self):
        input_dataframe = self.sqlCtx.createDataFrame(SAMPLE_DATA, BASE_COLUMNS)
        expected_df = self.sqlCtx.createDataFrame(
            [ROW_2, ROW_3],
            BASE_COLUMNS
        )
        actual_df = price_analytics.find_books_in_price_range(input_dataframe, 100, 1000)
        self.assertEqual(expected_df.schema, actual_df.schema)
        self.assertEqual(expected_df.collect(), actual_df.collect())

    def test_should_return_all_books_grouped_by_year_in_ascending_order(self):
        input_dataframe = self.sqlCtx.createDataFrame(SAMPLE_DATA, BASE_COLUMNS)
        expected_df_1 = self.sqlCtx.createDataFrame(
            [ROW_1, ROW_4],
            BASE_COLUMNS
        )
        expected_df_2 = self.sqlCtx.createDataFrame(
            [ROW_2, ROW_3],
            BASE_COLUMNS
        )
        expected_dict = {
            '2007': expected_df_1,
            '2017': expected_df_2
        }
        actual_dict = aggregated_views.aggregate_by_year(input_dataframe)
        self.assertEqual(expected_dict['2007'].schema, actual_dict['2007'].schema)
        self.assertEqual(expected_dict['2007'].collect(), actual_dict['2007'].collect())
        self.assertEqual(expected_dict['2017'].schema, actual_dict['2017'].schema)
        self.assertEqual(expected_dict['2017'].collect(), actual_dict['2017'].collect())

    def test_should_return_books_from_one_year_grouped_by_year_in_ascending_order(self):
        input_dataframe = self.sqlCtx.createDataFrame(SAMPLE_DATA, BASE_COLUMNS)
        expected_df = self.sqlCtx.createDataFrame(
            [ROW_1, ROW_4],
            BASE_COLUMNS
        )
        expected_dict = {
            '2007': expected_df
        }
        actual_dict = aggregated_views.aggregate_by_year(input_dataframe, 2007)
        self.assertEqual(expected_dict['2007'].schema, actual_dict['2007'].schema)
        self.assertEqual(expected_dict['2007'].collect(), actual_dict['2007'].collect())

    def test_should_return_all_books_grouped_by_author_in_ascending_order(self):
        input_dataframe = self.sqlCtx.createDataFrame(SAMPLE_DATA, BASE_COLUMNS)
        expected_df_1 = self.sqlCtx.createDataFrame(
            [ROW_2],
            BASE_COLUMNS
        )
        expected_df_2 = self.sqlCtx.createDataFrame(
            [ROW_1, ROW_3],
            BASE_COLUMNS
        )
        expected_df_3 = self.sqlCtx.createDataFrame(
            [ROW_4],
            BASE_COLUMNS
        )
        expected_dict = {
            "Al Rae": expected_df_1,
            "Johnny Johnson": expected_df_2,
            "Quack Quack": expected_df_3
        }
        actual_dict = aggregated_views.aggregate_by_author(input_dataframe)
        self.assertEqual(expected_dict['Al Rae'].schema, actual_dict['Al Rae'].schema)
        self.assertEqual(expected_dict['Al Rae'].collect(), actual_dict['Al Rae'].collect())
        self.assertEqual(expected_dict['Johnny Johnson'].schema, actual_dict['Johnny Johnson'].schema)
        self.assertEqual(expected_dict['Johnny Johnson'].collect(), actual_dict['Johnny Johnson'].collect())
        self.assertEqual(expected_dict['Quack Quack'].schema, actual_dict['Quack Quack'].schema)
        self.assertEqual(expected_dict['Quack Quack'].collect(), actual_dict['Quack Quack'].collect())

    def test_should_return_books_from_one_author_grouped_by_authour_in_ascending_order(self):
        input_dataframe = self.sqlCtx.createDataFrame(SAMPLE_DATA, BASE_COLUMNS)
        expected_df = self.sqlCtx.createDataFrame(
            [ROW_1, ROW_3],
            BASE_COLUMNS
        )
        expected_dict = {
            "Johnny Johnson": expected_df
        }
        actual_dict = aggregated_views.aggregate_by_author(input_dataframe, "Johnny Johnson")
        self.assertEqual(expected_dict['Johnny Johnson'].schema, actual_dict['Johnny Johnson'].schema)
        self.assertEqual(expected_dict['Johnny Johnson'].collect(), actual_dict['Johnny Johnson'].collect())

    def test_should_serialize_json_given_dataframe(self):
        example_df = self.sqlCtx.createDataFrame(
            [ROW_1, ROW_2],
            BASE_COLUMNS
        )
        expected_json = json.loads(json.dumps({"test": SAMPLE_JSON}))
        actual_json = json.loads(utils.json_from_df("test", example_df))
        self.assertEqual(expected_json, actual_json)

    def test_should_serialize_json_given_dictionary_of_dataframes(self):
        example_df = self.sqlCtx.createDataFrame(
            [ROW_1, ROW_2],
            BASE_COLUMNS
        )
        expected_json = json.loads(json.dumps({"test1": SAMPLE_JSON, "test2": SAMPLE_JSON}))
        actual_json = json.loads(utils.json_from_dict({"test1": example_df, "test2": example_df}))
        self.assertEqual(expected_json, actual_json)
