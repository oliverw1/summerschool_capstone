import json

import boto3

_bucket = "dm-summer-capstone"


def write_json_to_s3_object(json_object: dict, key: str):
    s3 = boto3.client("s3")
    s3.put_object(Body=str(json.dumps(json_object)), Bucket=_bucket, Key=key)


def get_spark_datalink(key: str):
    return f"s3a://{_bucket}/{key}"
