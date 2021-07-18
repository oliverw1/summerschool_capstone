import pyspark.sql
from pyspark.sql import SparkSession


def read_json_as_df(spark: SparkSession, path: str):
    df = spark.read.json(path)
    return df


def flatten_df():
    def inner(df: pyspark.sql.DataFrame):
        flat_cols = [c[0] for c in df.dtypes if c[1][:6] != 'struct']
        nested_cols = [c[0] for c in df.dtypes if c[1][:6] == 'struct']
        flat_df = df.select(*flat_cols, *[c + ".*" for c in nested_cols])
        return flat_df
    return inner