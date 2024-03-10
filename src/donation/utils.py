from .api import DonationAlertsAPI
from .database._requests import get_tokens, set_tokens 
from .server import DONATION_CONFIG


async def refresh_tokens():
    tokens = await get_tokens()

    donation = DonationAlertsAPI(**DONATION_CONFIG)

    new_tokens = await donation.refresh_tokens(tokens.get("refresh"))
    await set_tokens(new_tokens.get("access"), new_tokens.get("refresh"))


async def get_donation_alerts_list():
    await refresh_tokens() 

    tokens = await get_tokens()
    alerts_list = await DonationAlertsAPI.get_donation_alerts_list(tokens.get("access"))

    return alerts_list 