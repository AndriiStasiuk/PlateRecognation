"""This module defines the service routing system."""

from sanic import Blueprint
from sanic.app import Sanic

from image_gw_api.constants import API_PREFIX
from image_gw_api.resources.image_processing_resource import ImageProcessing
from image_gw_api.resources.smoke_resource import SmokeResources


def load_api(app: Sanic) -> None:
    """...."""
    api_v1 = Blueprint("v1", url_prefix=API_PREFIX)

    api_v1.add_route(SmokeResources.as_view(), "/smoke", strict_slashes=False)
    api_v1.add_route(ImageProcessing.as_view(), "/image_processing", strict_slashes=False)

    app.blueprint(api_v1)
