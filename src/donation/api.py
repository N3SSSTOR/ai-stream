import aiohttp 

from ._types import Scope


class DonationAlertsAPI:

    def __init__(
        self,
        client_id: str,
        client_secret: str 
    ):
        self.client_id = client_id
        self.client_secret = client_secret

        self.base_url = "https://www.donationalerts.com/oauth"

    async def get_login_uri(self, redirect_uri: str, scope: Scope):
        return f"{self.base_url}/authorize" + \
               f"?client_id={self.client_id}" + \
               f"&redirect_uri={redirect_uri}" + \
               f"&response_type=code" + \
               f"&scope={scope}"

    async def authorize(self, redirect_uri: str, scope: Scope):
        url = "https://www.donationalerts.com/oauth/authorize"
        
        params = {
            "client_id": self.client_id,
            "redirect_uri": redirect_uri,
            "scope": scope,
            "response_type": "code" 
        }

        async with aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(ssl=False)
        ) as session:
            async with session.get(url, params=params) as response:
                return await response.text()