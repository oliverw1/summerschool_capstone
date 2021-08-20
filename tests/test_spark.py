import datetime

import pytz

from summer_capstone.util.spark import string_columns_to_timestamp, ClosableSparkSession


def test_string_to_timestamp():
    with ClosableSparkSession("test") as spark:
        date_string = "2021-03-10T22:59:47+00:00"
        df = spark.createDataFrame(
            data=[("1", date_string)],
            schema=["id", "timestamp"])
        df = df.transform(string_columns_to_timestamp({"timestamp"}))
        assert df.head()[1].astimezone(pytz.utc) == datetime.datetime.fromisoformat(date_string)
