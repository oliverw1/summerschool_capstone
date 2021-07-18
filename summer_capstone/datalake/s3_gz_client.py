import datetime
import gzip
import json
import logging
import os
import shutil

import boto3


class S3JsonGzClient:
    def __init__(self, bucket: str, prefix: str):
        self.bucket = bucket
        self.prefix = prefix

    def write(self, table, records, date: datetime, boto3_session=None, suffix=""):
        def local_json_filename(split_idx):
            return f"{table}{suffix}_{split_idx}.json"

        def local_json_gz_filename(split_idx):
            return f"{table}{suffix}_{split_idx}.json.gz"

        logging.info("Dumping json to local files")
        count = 0
        split = 0
        json_file = open(local_json_filename(split), "w")
        for record in records:
            json_file.write(json.dumps(record) + "\n")
            count += 1
            if count % 1000000 == 0:
                split += 1
                json_file.close()
                json_file = open(local_json_filename(split), "w")
        json_file.close()
        logging.info("Dumping done")

        logging.info("Zipping json files")
        for i in range(split + 1):
            with open(local_json_filename(i), "rb") as f_in:
                with gzip.open(local_json_gz_filename(i), "wb") as f_out:
                    shutil.copyfileobj(f_in, f_out)
        logging.info("Zipping done")

        s3 = boto3.client("s3") if boto3_session is None else boto3_session.client("s3")

        for i in range(split + 1):
            key = f"{self.prefix}/{table}/{date.year}/{date.month}/{date.day}/{table}{suffix}_{i}.json.gz"
            logging.info(f"Writing {key} to S3 {self.bucket}...")
            s3.put_object(
                Bucket=self.bucket,
                Key=key,
                ContentType="text/plain",
                ContentEncoding="gzip",
                Body=open(local_json_gz_filename(i), "rb"),
            )
            logging.info(f"Successfully written to S3.")
            os.remove(local_json_filename(i))
            os.remove(local_json_gz_filename(i))