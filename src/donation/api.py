import aiohttp 

from ._types import Scope


class DonationAlertsAPI:

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        redirect_uri: str,
        scope: Scope
    ) -> None:
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.scope = scope

        self.base_url = "https://www.donationalerts.com/oauth"

    async def get_login_uri(self) -> str:
        return f"{self.base_url}/authorize" + \
               f"?client_id={self.client_id}" + \
               f"&redirect_uri={self.redirect_uri}" + \
               f"&response_type=code" + \
               f"&scope={self.scope}"

    async def get_tokens(self, code: str) -> dict:
        async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(ssl=False)
        ) as session:
            data = {
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": self.redirect_uri,
                "scope": self.scope
            }

            async with session.post(f"{self.base_url}/token", data=data) as response:
                data = await response.json()
                return {
                    "access": data.get("access_token"),
                    "refresh": data.get("refresh_token"),
                }
            
    async def refresh_tokens(self, refresh_token: str) -> dict:
        async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(ssl=False)
        ) as session:
            data = {
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
                "scope": self.scope
            }
            async with session.post(f"{self.base_url}/token", data=data) as response:
                data = await response.json()
                return {
                    "access": data.get("access_token"),
                    "refresh": data.get("refresh_token"),
                }
            
    @staticmethod
    async def get_user(access_token: str) -> dict:
        async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(ssl=False)
        ) as session:
            url = " https://www.donationalerts.com/api/v1/user/oauth"
            headers = {
                "Authorization": f"Bearer {access_token}"
            }

            async with session.get(url, headers=headers) as response:
                return await response.json()
            
    @staticmethod
    async def get_donation_alerts_list(access_token: str) -> dict:
        async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(ssl=False)
        ) as session:
            url = "https://www.donationalerts.com/api/v1/alerts/donations"
            headers = {
                "Authorization": f"Bearer {access_token}"
            }

            async with session.get(url, headers=headers) as response:
                return await response.json()