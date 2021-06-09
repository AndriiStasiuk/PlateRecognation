FROM python:3.8-slim-buster

WORKDIR /image_gw_api

COPY ./ /image_gw_api

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install pip==19.3
RUN pip install -e .'[dev,test]'

EXPOSE 5000

ENTRYPOINT ["python3", "/image_gw_api/manage.py", "runserver"]
