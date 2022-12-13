import os

from deta import Deta
from dotenv import load_dotenv

# loading environment variable
load_dotenv(".env")
DETA_KEY = os.getenv("DETA_KEY")

deta = Deta(DETA_KEY)
# this is how to create/ connect database
db = deta.Base("monthly_reports")

def insert_period(period, contributions, investments, comment):
    """Returns the report on a successful creation, otherwise raises an error"""
    return db.put({"key": period, "contributions": contributions, "investments": investments, "comment": comment})

def fetch_all_periods():
    """Return a dict of all periods"""
    res = db.fetch()
    return res.items

def get_period(period):
    """If not found, function will return None"""
    return db.get(period)