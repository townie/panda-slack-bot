FROM resin/raspberrypi3-python


COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY . /usr/src/app
WORKDIR /usr/src/app

CMD ["python", "run.py"]