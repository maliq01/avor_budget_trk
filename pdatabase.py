import os

from deta import Deta
from dotenv import load_dotenv

load_dotenv(".env")
PDETA_KEY = os.getenv("PDETA_KEY")

deta = Deta(PDETA_KEY)

# creating a database
db = deta.Base("username_and_passwords")


def insert_username(username, password):
    """Returns the report on a successful creation, otherwise raises an error"""
    return db.put({"key": username, "password": password})


def fetch_all_username():
    """Return a dict of all username"""
    res = db.fetch()
    return res.items


def get_username(username):
    """If not found, function will return None"""
    return db.get(username)

