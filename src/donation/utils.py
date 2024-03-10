from .api import DonationAlertsAPI
from .database._requests import get_tokens, set_tokens 
from .server import DONATION_CONFIG


async def refresh_tokens():
    tokens = await get_tokens()

    donation = DonationAlertsAPI(**DONATION_CONFIG)

    new_tokens = await donation.refresh_tokens(tokens.get("refresh"))
    await set_tokens(new_tokens.get("access"), new_tokens.get("refresh"))


async def get_donations():
    await refresh_tokens() 

    tokens = await get_tokens()
    donations = await DonationAlertsAPI.get_donations(tokens.get("access"))

    return donations