import pytest
from summer_capstone.util.spark import ClosableSparkSession
from summer_capstone.db_export.export import read_json_as_df, flatten_df


@pytest.fixture(scope="module")
def spark():
    with ClosableSparkSession("test") as spark:
        yield spark


def test_read_json(spark):
    df = read_json_as_df(spark, "data/sample.json")
    assert df.count() == 2


def test_flatten_df(spark):
    df = read_json_as_df(spark, "data/sample.json")
    flat_df = df.transform(flatten_df())
    assert len(flat_df.columns) == 15
