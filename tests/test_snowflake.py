import json
import os

import boto3
import pytest
from moto import mock_secretsmanager

from summer_capstone.util.snowflake import get_snowflake_creds_from_sm

_region = "eu-west-1"

# Workaround for moto bug
os.environ["AWS_ACCESS_KEY_ID"] = "test"
os.environ["AWS_SECRET_ACCESS_KEY"] = "test"


@pytest.fixture
@mock_secretsmanager
def secrets_manager_with_secret():
    session = boto3.Session(region_name=_region)
    sm_client = session.client("secretsmanager")
    sm_client.create_secret(Name="dummy",
                            SecretString=json.dumps({
                                "URL": "link",
                                "USER_NAME": "USER",
                                "PASSWORD": "PASS"
                            }))
    yield session
    sm_client.delete_secret(
        SecretId='dummy',
        ForceDeleteWithoutRecovery=True
    )

@mock_secretsmanager
def test_get_snowflake_creds(secrets_manager_with_secret):
    creds = get_snowflake_creds_from_sm("dummy", next(secrets_manager_with_secret))
    assert creds["sfURL"] == "link.snowflakecomputing.com"
    assert creds["sfPassword"] == "PASS"
    assert creds["sfUser"] == "USER"
