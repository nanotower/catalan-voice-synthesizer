import yaml
import logging
import logging.config
from auth import TokenAuth
from routes import speech, token_req, health
from starlette.middleware import Middleware
from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.routing import Route

#Initialize logger from config file
with open('config/logging.yml', 'r') as f:
    log_cfg = yaml.safe_load(f.read())
    logging.config.dictConfig(log_cfg)
    logger = logging.getLogger("voice")


#Init server
routes = [
    Route("/", methods=["POST"], endpoint=speech.speech),
    Route("/token",  methods=["POST"], endpoint=token_req.login_for_access_token),
    Route("/test", endpoint=health.check)
]
middleware = [
    Middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*']),
    Middleware(AuthenticationMiddleware, backend=TokenAuth.BackendMiddleware())
]
app = Starlette(debug=True, middleware=middleware, routes=routes)


logger.info("Listening")