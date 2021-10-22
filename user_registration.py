import redis
import json
import argparse
from passlib.context import CryptContext

with open("./config/config.json") as f:
    conf = json.load(f)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
name_space = "users_db"

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def main(args):
    hashed_password = get_password_hash(args.password)

    user_dict = {"username": args.username, "hashed_password": hashed_password, "active": 1}
    user_json = json.dumps(user_dict)

    r = redis.Redis(host=conf["redis_host"], port=conf["redis_port"], db=conf["redis_db"], decode_responses=True)

    user_exists = r.hexists(name_space, args.user_id)

    if user_exists:
        raise ValueError('User id already exists')

    user_in_db = r.hset(name_space, args.user_id, user_json)
    print(f"User successful created: {user_in_db}")

    get_user_db = r.hget(name_space, args.user_id)
    print(f"User created: {get_user_db}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--user_id', help='New user id')
    parser.add_argument('--username', help='New user name')
    parser.add_argument('--password', help='New user password')

    args = parser.parse_args()

    if not (args.user_id or args.username or args.password):
        raise ValueError('user_id, username and password needs to be given')

    main(args)


    # name_space = "users_db"
    # user_id = 2
    # username = 'test2'
    # password = 'fd468069ebfc6cbb848bb673541c18ef979c6f2a2e5998481f2c524f0fb3257a'
