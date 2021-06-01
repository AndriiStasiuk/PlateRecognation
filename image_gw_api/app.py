"""Module which execute needed operations before server start and after server stop."""

from sanic.app import Sanic
from sanic_cors import CORS
from image_gw_api.configurations import DevConfig
import aiohttp

from image_gw_api.api_v1 import load_api
from image_gw_api.constants import SERVICE_NAME

app = Sanic(SERVICE_NAME)
app.config.from_object(DevConfig)


@app.listener("before_server_start")
def init(async_app, loop):
    async_app.aiohttp_session = aiohttp.ClientSession(loop=loop)


@app.listener("after_server_stop")
def finish(async_app, loop):
    loop.run_until_complete(async_app.aiohttp_session.close())
    loop.close()


cors = CORS(
    app,
    resources={r"*": {"origin": "*"}},
    expose_headers=[
        "Link, X-Pagination-Current-Page",
        "X-Pagination-Per-Page",
        "X-Pagination-Total-Count",
        "X-Client",
        "Authorization",
        "Content-Type",
        "X-Filename",
    ],
)

load_api(app)
