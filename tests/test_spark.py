import datetime

from summer_capstone.util.spark import string_columns_to_timestamp, ClosableSparkSession


def test_string_to_timestamp():
    with ClosableSparkSession("test") as spark:
        df = spark.createDataFrame(
            data=[("1", "2021-03-10T22:59:47-00:00")],
            schema=["id", "timestamp"])
        df = df.transform(string_columns_to_timestamp({"timestamp"}))
        assert df.collect()[0][1] == datetime.datetime(2021, 3, 10, 23, 59, 47)
