"""This module contains basic classes for configuring service and test if service is available."""

import cv2
import numpy as np
from sanic.response import json
from sanic.views import HTTPMethodView

from image_gw_api.utils.image_processor import ImageProcessor
from image_gw_api.utils.logger import log
import aiohttp


class ImageProcessing(HTTPMethodView):

    async def post(self, request):
        await log.info("Going to process image")
        image = request.files.get("image").body
        image_processor = ImageProcessor(cv2.imdecode(np.frombuffer(image, np.uint8), -1))
        car_plate = image_processor.process_image()
        await log.info("Image was processed successfully, sent request to get needed info related to the car")
        url = f"http://127.0.0.1:5001/gw_info/v1/transport?car_plate={car_plate}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers={}) as response:
                try:
                    car_info = await response.json()
                except Exception as e:
                    await log.error(f"Unable to retrieve data: {e}")
                    return await response.text()

        return json({"car_info": car_info["message"]}, status=200)
