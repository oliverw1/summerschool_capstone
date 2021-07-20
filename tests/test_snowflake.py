import json

import boto3
import pytest
from moto import mock_secretsmanager

from summer_capstone.util.snowflake import get_snowflake_creds_from_sm

_region = "eu-west-1"


@mock_secretsmanager
@pytest.fixture
def secrets_manager_with_secret():
    sm_client = boto3.client("secretsmanager", region_name=_region)
    yield sm_client.create_secret(Name="dummy",
                                  SecretString=json.dumps({
                                      "URL": "link",
                                      "USER_NAME": "USER",
                                      "PASSWORD": "PASS"
                                  }))
    sm_client.delete_secret(
        SecretId='dummy',
        ForceDeleteWithoutRecovery=True
    )


def test_get_snowflake_creds(secrets_manager_with_secret):
    creds = get_snowflake_creds_from_sm("dummy", _region)
    assert creds["sfURL"] == "link.snowflakecomputing.com"
    assert creds["sfPassword"] == "PASS"
    assert creds["sfUser"] == "USER"
