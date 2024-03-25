import uvicorn
from fastapi import FastAPI, responses

from config import DONATION_ID, DONATION_SECRET
from .api import DonationAlertsAPI
from ._types import Scope 
from .database._requests import set_tokens

DONATION_CONFIG = dict(
    client_id=DONATION_ID, 
    client_secret=DONATION_SECRET,
    redirect_uri="http://127.0.0.1:5000/login",
    scope=Scope.DONATION_INDEX.value
)

app = FastAPI()


@app.get("/")
async def root():
    donation = DonationAlertsAPI(**DONATION_CONFIG)
    login_uri = await donation.get_login_uri()
    return responses.RedirectResponse(login_uri)


@app.get("/login")
async def login(code: str):
    donation = DonationAlertsAPI(**DONATION_CONFIG)
    tokens = await donation.get_tokens(code)

    await set_tokens(tokens.get("access"), tokens.get("refresh"))
    return tokens 


def run_server():
    uvicorn.run(app, host="0.0.0.0", port=5000)