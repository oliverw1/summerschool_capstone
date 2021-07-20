import awswrangler as wr
import boto3


def get_snowflake_creds_from_sm(secret_name: str, region: str):
    b_session =boto3.Session(region_name=region)
    creds = wr.secretsmanager.get_secret_json(secret_name, b_session)
    return {
        "sfURL": f"{creds['URL']}.snowflakecomputing.com",
        "sfPassword": creds["PASSWORD"],
        "sfUser": creds["USER_NAME"]
    }
