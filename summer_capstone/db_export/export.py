import pyspark.sql
from pyspark.sql import SparkSession


def read_json_as_df(spark: SparkSession, path: str):
    df = spark.read.json(path)
    return df


def flatten_df(df: pyspark.sql.DataFrame):
    flat_cols = [colname for colname, datatype in df.dtypes if not datatype.startswith('struct')]
    nested_cols = [colname for colname, datatype in df.dtypes if datatype.startswith('struct')]
    return df.select(*flat_cols, *[c + ".*" for c in nested_cols])
