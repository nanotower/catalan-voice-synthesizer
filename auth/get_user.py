import json
from auth.auth_types import UserInDB
from handlers.Db import Db

with open("./config/config.json") as f:
    configuration = json.load(f)

def get_user(username:str):
    db = Db(configuration)
    if db.dbuser_exists(username):
        user_dict = db.get_dbuser(username)
        user_dict = json.loads(user_dict)
        return UserInDB(**user_dict)
