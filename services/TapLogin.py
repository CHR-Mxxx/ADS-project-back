import requests
import json
import hashlib
import urllib.parse
import time
import uuid
import asyncio

# import aiohttp
import hmac
import base64
import os
import qrcode
from io import BytesIO, StringIO


class CompleteQRCodeData:
    def __init__(self, deviceId, device_code, expires_in, qrcode_url, interval):
        self.deviceID = deviceId
        self.deviceCode = device_code
        self.expiresInSeconds = expires_in
        self.url = qrcode_url
        self.interval = interval


AppKey = "Qr9AEqtuoSVS3zeD6iVbM4ZC0AtkJcQ89tywVyi0"
ClientId = "rAK3FfdieFob2Nn8Am"


class LCHelper:
    def __init__(self):
        pass

    def md5HashHexStringDefaultGetter(self, input):
        return hashlib.md5(input).hexdigest()

    async def loginWithAuthData(self, data, failOnNotExist=False):
        authData = {"taptap": data}
        if failOnNotExist:
            path = "users?failOnNotExist=true"
        else:
            path = "users"
        response = await self.request(path, "post", data={authData})
        return response

    async def loginAndGetToken(self, data, failOnNotExist=False):
        response = await self.loginWithAuthData(data, failOnNotExist)
        return response

    async def request(
        self, path, method, data=None, queryParams=None, withAPIVersion=True
    ):
        url = "https://rak3ffdi.cloud.tds1.tapapis.cn/1.1/users"
        headers = {"X-LC-Id": ClientId, "Content-Type": "application/json"}
        self.fillHeaders(headers)
        response = await requests.request(method, url, data=json.dump(data))
        return response

    def buildUrl(self, path, queryParams, withAPIVersion):
        url = "https://rak3ffdi.cloud.tds1.tapapis.cn"

        if withAPIVersion:
            url += "/1.1"
        url += f"/{path}"

        if queryParams:
            filtered_params = {k: v for k, v in queryParams.items() if v is not None}

        if filtered_params:
            queryString = urllib.parse.urlencode(filtered_params)
            url += f"?{queryString}"
        return url

    def fillHeaders(self, headers, req_headers=None):
        if req_headers is not None:
            for key, value in req_headers.items():
                headers[key] = str(value)

        timestamp = int(time.time())
        data = f"{timestamp}{AppKey}"
        hash_md5 = hashlib.md5(data.encode("utf-8")).hexdigest()
        sign = f"{hash_md5},{timestamp}"
        headers["X-LC-Sign"] = sign

        return headers


class TapTapHelper:
    def __init__(self):
        self.TapSDKVersion = "2.1"
        self.WebHost = "https://accounts.tapapis.com"
        self.ChinaWebHost = "https://accounts.tapapis.cn"
        self.ApiHost = "https://open.tapapis.com"
        self.ChinaApiHost = "https://open.tapapis.cn"
        self.CodeUrl = f"{self.WebHost}/oauth2/v1/device/code"
        self.ChinaCodeUrl = f"{self.ChinaWebHost}/oauth2/v1/device/code"
        self.TokenUrl = f"{self.WebHost}/oauth2/v1/token"
        self.ChinaTokenUrl = f" {self.ChinaWebHost}/oauth2/v1/token"

    def GetChinaProfiler(self, havePublicProfile=True):
        if havePublicProfile:
            return self.ChinaApiHost + "account/profile/v1?client_id="
        else:
            return self.ChinaApiHost

    def requestLoginQrCode(self, permissions=["public_profile"], useChinaEndpoint=True):
        clientId = str(uuid.uuid4()).replace("-", "")
        params = {
            "client_id": "rAK3FfdieFob2Nn8Am",
            "response_type": "device_code",
            "scope": ",".join(permissions),
            "version": self.TapSDKVersion,
            "platform": "unity",
            "info": json.dumps({"device_id": clientId}),
        }

        if useChinaEndpoint:
            endpoint = self.ChinaCodeUrl
        else:
            endpoint = self.CodeUrl

        response = requests.post(endpoint, data=params)
        data = response.json()
        return {**data, "deviceId": clientId}

    async def checkQRCodeResult(self, data, useChinaEndpoint=True):
        qrCodeData = CompleteQRCodeData(data)
        params = {
            "grant_type": "device_token",
            "client_id": "rAK3FfdieFob2Nn8Am",
            "secret_type": "hmac-sha-1",
            "code": qrCodeData.deviceCode,
            "version": "1.0",
            "platform": "unity",
            "info": json.dumps({"device_id": qrCodeData.deviceID}),
        }
        if useChinaEndpoint:
            endpoint = self.ChinaTokenUrl
        else:
            endpoint = self.TokenUrl
        try:
            response = await requests.post(endpoint, data=params)
            data = await response.json()
            return data
        except Exception as err:
            # Handle error here
            print(f"Error checking QR code result:{err}")
            return None

    async def getProfile(self, token, useChinaEndpoint=True, timestamp=0):
        if "public_profile" not in token.get("scope", ""):
            raise ValueError("Public profile permission is required.")

        if useChinaEndpoint:
            url = f"{self.ChinaApiHost}/account/profile/v1?client_id=rAK3FfdieFob2Nn8Am"  # Replace with actual client ID
        else:
            url = f"{self.ApiHost}/account/profile/v1?client_id=rAK3FfdieFob2Nn8Am"  # Replace with actual client ID

        # if not timestamp {
        #     let now = new Date()
        #     timestamp = Math.floor(now.getTime() / 1000).padStart(10, '0')
        # }

        # let macKey = CryptoJS.enc.Hex.parse(token.mac_key) # Convert hex string to WordArray for CryptoJS
        # let macAlgorithm = token.mac_algorithm
        method = "GET"
        # let uri = url
        # let host = new URL(url).hostname
        # let port = '443'

        # let nonce = Math.random().toString()
        # let normalizedString = `${timestamp}\n${nonce}\n${method}\n${uri}\n${host}\n${port}\n\n`

        # let hash
        # switch (macAlgorithm) {
        #     case 'hmac-sha-256':
        #         hash = CryptoJS.HmacSHA256(normalizedString, macKey).toString(CryptoJS.enc.Base64)
        #         break
        #     case 'hmac-sha-1':
        #         hash = CryptoJS.HmacSHA1(normalizedString, macKey).toString(CryptoJS.enc.Base64)
        #         break
        #     default:
        #         throw new Error(`Unsupported MAC algorithm: ${macAlgorithm}`)
        # }

        authorizationHeader = self.getAuthorization(
            url, method, token.kid, token.mac_key
        )
        # let authorizationHeader = `MAC id="${token.kid}",ts="${timestamp}",nonce="${nonce}",mac="${hash}"`

        response = await requests.request(
            url,
            {
                "method": "GET",
                "headers": {"Authorization": authorizationHeader},
            },
        )

        return response.json()

    def getAuthorization(self, requestUrl, method, keyId, macKey):
        url = urllib.parse.urlparse(requestUrl)
        timestamp = str(int(time.time())).zfill(10)
        randomStr = self.getRandomString(16)
        host = url["hostname"]
        uri = url["pathname"] + url["search"]
        port = url["port"] or ("443" if url["scheme"] == "https" else "80")
        other = ""
        sign = self.signData(
            self.mergeData(timestamp, randomStr, method, uri, host, port, other), macKey
        )
        return f'MAC id="{keyId}", ts="{timestamp}", nonce="{randomStr}", mac="{sign}"'

    def getRandomString(self, length):
        random_bytes = os.urandom(length)
        return base64.b64encode(random_bytes).decode("utf-8")[:length]

    def mergeData(self, timestamp, random_code, http_type, uri, domain, port, other):
        prefix = f"{timestamp}\n{random_code}\n{http_type}\n{uri}\n{domain}\n{port}\n"
        if not other:
            prefix += "\n"
        else:
            prefix += f"{other}\n"

        return prefix

    def signData(self, signature_base_string, key):
        # 确保密钥是字节串
        if isinstance(key, str):
            key = key.encode("utf-8")

        # 确保字符串是字节串
        if isinstance(signature_base_string, str):
            signature_base_string = signature_base_string.encode("utf-8")

        # 使用HMAC-SHA1进行签名
        hmac_digest = hmac.new(key, signature_base_string, hashlib.sha1).digest()

        # Base64编码
        return base64.b64encode(hmac_digest).decode("utf-8")


class getQRcode:
    async def getRequest(self):
        return await TapTapHelper.requestLoginQrCode()

    async def getQRcode(self, url):
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image()
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        return buffer.getvalue()

    async def checkQRCodeResult(self, request):
        return await TapTapHelper.checkQRCodeResult(request)

    async def getProfile(self, result):
        return await TapTapHelper.getProfile(result["data"])

    async def getSessionToken(self, profile, result):
        return await LCHelper.loginAndGetToken({**profile["data"], **result["data"]})


TapHelper = TapTapHelper()
Partial = TapHelper.requestLoginQrCode()
print("partial:", Partial)

getQrCodeBuffer = getQRcode()
qrCodeBuffer = getQrCodeBuffer.getQRcode(Partial["data"]["qrcode_url"])
with open("qrcode.png", "bw") as f:
    f.write(qrCodeBuffer)

result = TapTapHelper.checkQRCodeResult(Partial)

while not result["success"]:
    asyncio.sleep(2)
    result = TapTapHelper.checkQRCodeResult(Partial)
    print(result)

print(result)

# # let result = {
# #     kid: '1/O_I6HWAwQyDprWXujXgC65ZxipruCZAe_EcR565m7Zek6oLalJtLzH1K_cJyPX_4Mue0QgLp5RQfr4mf4FhYWavnNkyy_YnZqJDwDn4YEP2kcZny9aoIGUH_QFpVL9awF7AAq1iQCHketsTCzWUfzyVDaald526BVrYAiQUzasXQn29sY19oVoAJwJpxjlYBTX1Jr7PXrFOBreYlg213hRtzYnFcX3RHIkpZO9Qo86jPxfIqR7wHdh74sD0ZZ-808Rf5hg3ITfPa30a7h36XUhd1ikpVHGsbG0nYm5mb8JKc2C5Qq0mbGCIap5YVtHLL2BUbKpniDKwiWgsbpcRBDw',
# #     access_token: '1/O_I6HWAwQyDprWXujXgC65ZxipruCZAe_EcR565m7Zek6oLalJtLzH1K_cJyPX_4Mue0QgLp5RQfr4mf4FhYWavnNkyy_YnZqJDwDn4YEP2kcZny9aoIGUH_QFpVL9awF7AAq1iQCHketsTCzWUfzyVDaald526BVrYAiQUzasXQn29sY19oVoAJwJpxjlYBTX1Jr7PXrFOBreYlg213hRtzYnFcX3RHIkpZO9Qo86jPxfIqR7wHdh74sD0ZZ-808Rf5hg3ITfPa30a7h36XUhd1ikpVHGsbG0nYm5mb8JKc2C5Qq0mbGCIap5YVtHLL2BUbKpniDKwiWgsbpcRBDw',
# #     token_type: 'mac',
# #     mac_key: 'zCgtfVWxajWHl2MYVoFMNdPn0E2YXrV4mTjWjLKp',
# #     mac_algorithm: 'hmac-sha-1',
# #     scope: 'public_profile'
# # }

profile = TapTapHelper.getProfile(result["data"])
# # let profile = await TapTapHelper.getProfile(result)
print(profile)


sessionToken = LCHelper.loginAndGetToken({**profile["data"], **result["data"]})
print(sessionToken)

asyncio.run()
