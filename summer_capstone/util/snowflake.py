import awswrangler as wr
import boto3


def get_snowflake_creds_from_sm(secret_name: str, b3_session):
    creds = wr.secretsmanager.get_secret_json(secret_name, b3_session)
    return {
        "sfURL": f"{creds['URL']}.snowflakecomputing.com",
        "sfPassword": creds["PASSWORD"],
        "sfUser": creds["USER_NAME"]
    }
