import logging

import dateutil.tz
import pyspark.sql
from pyspark.sql import SparkSession
import pyspark.sql.functions as F


def string_columns_to_timestamp(col_names: set, format="yyyy-MM-dd'T'HH:mm:ssXXX"):
    def inner(df: pyspark.sql.DataFrame):
        for c_name in col_names:
            df = df.withColumn(c_name,
                               F.to_timestamp(c_name, format=format))
        return df

    return inner


def write_df_with_options(df, format: str, mode: str, options: dict):
    (df.write.format(format)
     .options(**options)
     .mode(mode)
     .save())


class ClosableSparkSession:
    def __init__(
            self,
            app_name: str,
            master: str = None,
            spark_config: dict = {},
    ):
        self._app_name = app_name
        self._master = master
        self._spark_config = spark_config
        self._spark_session = None

    def __enter__(self):
        spark_builder = SparkSession.builder.appName(self._app_name).enableHiveSupport()

        # set master if needed
        if self._master:
            spark_builder = spark_builder.master(self._master)

        # set some default configuration
        spark_builder.config("spark.sql.sources.partitionOverwriteMode", "dynamic")
        spark_builder.config("fs.s3.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")

        # add other config params
        for key, val in self._spark_config.items():
            spark_builder.config(key, val)

        # create the actual session
        self._spark_session = spark_builder.getOrCreate()

        return self._spark_session

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_tb:
            logging.error(exc_tb)
        if self._spark_session:
            self._spark_session.stop()
