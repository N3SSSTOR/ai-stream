import uvicorn
from fastapi import FastAPI, responses

from .api import DonationAlertsAPI
from ._types import Scope 

CLIENT_ID = "12466"
CLIENT_SECRET = "1swGklN70ErQ59QmAXuEKO6ahqp6T1Mnxjby8cik"

app = FastAPI()


@app.get("/")
async def root():
    donation = DonationAlertsAPI(
        client_id=CLIENT_ID, 
        client_secret=CLIENT_SECRET
    )
    login_uri = await donation.get_login_uri(
        redirect_uri="http://127.0.0.1:5000/login",
        scope=Scope.USER_SHOW.value 
    )
    return responses.RedirectResponse(login_uri)


@app.get("/login")
async def login(code: str):
    return code 


def run_server():
    uvicorn.run(app, port=5000)