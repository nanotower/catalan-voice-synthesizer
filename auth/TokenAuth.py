import os
import jwt
import json
import logging
import binascii
from pydantic import BaseModel
from typing import Optional
from auth.get_user import get_user
from auth.auth_types import TokenData
from utilities import Monitor_Logger
from starlette.authentication import (
    AuthenticationBackend, AuthenticationError, SimpleUser, AuthCredentials
)

secret_key = os.getenv("SECRET_KEY")
auth_algorithm = os.getenv("AUTH_ALGORITHM")

with open("./config/config.json") as f:
    configuration = json.load(f)

#Monitorlog
logging.debug("Loading token middleware monitoring...")
monitor_log = configuration['monitor_log']
monitor = Monitor_Logger.Monitor_Logger(monitor_log)


class BackendMiddleware(AuthenticationBackend):

    async def authenticate(self, request):

        if "Authorization" not in request.headers:
            return

        auth = request.headers["Authorization"]

        scheme, credentials = auth.split()

        try:
            scheme, credentials = auth.split()
            if scheme.lower() != 'bearer':
                return
            decoded = jwt.decode(credentials, secret_key, algorithms=[auth_algorithm])

        except jwt.ExpiredSignatureError:
            monitor.add_token_expired_error()
            raise AuthenticationError('Signature has expired')

        except jwt.InvalidSignatureError:
            monitor.add_token_mid_error()
            raise AuthenticationError("Signature verification failed")

        except jwt.DecodeError:
            monitor.add_token_mid_error()
            raise AuthenticationError("Invalid header string")

        except (ValueError, UnicodeDecodeError, binascii.Error) as exc:
            monitor.add_token_mid_error()
            raise AuthenticationError('Invalid bearer auth token')

        username: str = decoded["sub"]

        if username is None:
            monitor.invalid_user_error()
            raise AuthenticationError('No user')

        token_data = TokenData(username=username)

        user = get_user( username=token_data.username)

        if user is None:
            monitor.invalid_user_error()
            raise AuthenticationError('Invalid user')
        

        return AuthCredentials(["authenticated"]), SimpleUser(user.username)

    