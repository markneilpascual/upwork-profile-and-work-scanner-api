from fastapi import FastAPI
from scraper.scraping import Scraping

app = FastAPI()
scrap = Scraping()


@app.get("/profile")
def profile():
    return scrap.get_profile_content()


@app.get("/works")
def works():
    return scrap.get_portal_content()

