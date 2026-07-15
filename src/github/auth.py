"""Github authentication."""

import os
import requests
from dotenv import load_dotenv
import urllib.parse
from src.models import (
    GithubDeviceFlowInitRequestModel,
    GithubDeviceFlowOAuthResponseModel,
)


def get_client_id() -> str | None:
    """Return the token set in the .env file."""
    load_dotenv()
    client_id = os.environ.get("GH_CLIENT_ID")
    return client_id


def get_gh_token() -> str | None:
    load_dotenv()
    gh_token = os.environ.get("GH_TOKEN")
    return gh_token


def parse_gh_device_flow_init_response(
    response_json: dict,
) -> GithubDeviceFlowInitRequestModel:
    """Parse the response data from a device flow init and return as a model."""
    response_json["verification_uri"] = urllib.parse.unquote(
        response_json["verification_uri"]
    )
    return GithubDeviceFlowInitRequestModel.model_validate(response_json)


def init_gh_auth() -> GithubDeviceFlowInitRequestModel:
    url = "https://github.com/login/device/code"
    data = {"client_id": get_client_id(), "scope": "read:user"}
    data = {"client_id": "Ov23liC9GAbdipRfBnlt", "scope": "read:user"}
    hdrs = {"Content-Type": "application/json", "Accept": "application/json"}
    r = requests.post(url, json=data, headers=hdrs, timeout=10)
    r.raise_for_status()
    return parse_gh_device_flow_init_response(r.json())


def check_token(device_code: str) -> GithubDeviceFlowOAuthResponseModel:
    url = "https://github.com/login/oauth/access_token"
    data = {
        "client_id": get_client_id(),
        "device_code": device_code,
        "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
    }
    hdrs = {"Content-Type": "application/json", "Accept": "application/json"}
    r = requests.post(url, json=data, headers=hdrs, timeout=10)
    r.raise_for_status()
    return GithubDeviceFlowOAuthResponseModel.model_validate(r.json())
