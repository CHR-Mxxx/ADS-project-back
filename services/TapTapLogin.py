import hmac
import base64
import json
import time
import random
import requests


class Share:
    def __init__(self):
        self.client = requests.Session()
        self.tap_headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "TapTapAndroidSDK/3.16.5",
        }
        self.phi_headers = {
            "User-Agent": "LeanCloud-CSharp-SDK/1.0.3",
            "X-LC-Id": "rAK3FfdieFob2Nn8Am",
            "X-LC-Key": "Qr9AEqtuoSVS3zeD6iVbM4ZC0AtkJcQ89tywVyi0",
            "Content-Type": "application/json",
        }


share = Share()


def mac(token):
    ts = int(time.time())
    nonce = random.randint(0, 2**32 - 1)
    input_str = f"{ts}\n{nonce}\nGET\n/account/basic-info/v1?client_id=rAK3FfdieFob2Nn8Am\nopen.tapapis.cn\n443\n\n"

    _mac = hmac.new(token["mac_key"].encode(), input_str.encode(), digestmod="sha1")
    mac_base64 = base64.b64encode(_mac.digest()).decode()

    return (
        f"MAC id=\"{token['kid']}\",ts=\"{ts}\",nonce=\"{nonce}\",mac=\"{mac_base64}\""
    )


async def get_account_info(token):
    url = "https://open.tapapis.cn/account/basic-info/v1?client_id=rAK3FfdieFob2Nn8Am"
    headers = share.tap_headers.copy()
    headers["Authorization"] = mac(token)

    response = share.client.get(url, headers=headers)
    json_response = response.json()

    return json_response["data"]


async def register_user(token, account):
    url = "https://rak3ffdi.cloud.tds1.tapapis.cn/1.1/users"
    headers = share.phi_headers
    payload = json.dumps(
        {
            "authData": {
                "taptap": {
                    "kid": token["kid"],
                    "access_token": token["kid"],
                    "token_type": "mac",
                    "mac_key": token["mac_key"],
                    "mac_algorithm": "hmac-sha-1",
                    "openid": account["openid"],
                    "unionid": account["unionid"],
                }
            }
        }
    )

    response = share.client.post(url, headers=headers, data=payload)
    return response.text
