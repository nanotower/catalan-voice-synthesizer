import os
import json
import logging
from auth import TokenAuth, token, authenticate
from utilities import Monitor_Logger
from datetime import datetime, timedelta
from starlette.responses import JSONResponse
from starlette.exceptions import HTTPException
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

with open("./config/config.json") as f:
    configuration = json.load(f)

#Monitorlog
logging.debug("Loading token req monitoring...")
monitor_log = configuration['monitor_log']
monitor = Monitor_Logger.Monitor_Logger(monitor_log)

token_expire_minutes = int(os.getenv("TOKEN_EXPIRE_MINUTES", "5"))

async def login_for_access_token(request):
    monitor.add_token_request()

    try:
        req_json = await request.json()
        user_id = req_json["user"]
        password = req_json["password"]
    except ValueError:
        error_msg = "Cannot parse request body request"
        logging.error(error_msg)
        monitor.add_reqtoken_error()
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=error_msg)
    except KeyError:
        error_msg = "user and password are required"
        logging.error(error_msg)
        monitor.add_reqtoken_error()
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=error_msg)

    user = authenticate.user(user_id, password)

    if not user:
        logging.error("Usuario no autorizado: {user_id}")
        monitor.add_reqtoken_error()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=token_expire_minutes)

    access_token = token.create_access_token(
        data={"sub": user_id}, expires_delta=access_token_expires
    )

    logging.info(f"Requested token user_id: {user_id}, user name: {user.username}")
    return JSONResponse({"access_token": access_token, "token_type": "bearer"})