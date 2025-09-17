from os import environ

import boto3
from fastmcp.server.auth.providers.google import GoogleProvider

GOOGLE_CLIENT_ID = environ["MEOW_GOOGLE_CLIENT_ID"]
GOOGLE_CLIENT_SECRET_ID = environ["MEOW_GOOGLE_CLIENT_SECRET_ID"]

if (APP_URL := environ.get("MEOW_APP_URL", None)) is None:
    APP_URL = boto3.client("lambda").get_function_url_config(
        FunctionName=environ["AWS_LAMBDA_FUNCTION_NAME"]
    )["FunctionUrl"]

GOOGLE_CLIENT_SECRET = boto3.client(service_name="secretsmanager").get_secret_value(
    SecretId=GOOGLE_CLIENT_SECRET_ID,
)["SecretString"]

print(f"GOOGLE_CLIENT_ID: {GOOGLE_CLIENT_ID}")
print(f"GOOGLE_CLIENT_SECRET: {GOOGLE_CLIENT_SECRET}")
print(f"APP_URL: {APP_URL}")


auth = GoogleProvider(
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    base_url=APP_URL,
)
