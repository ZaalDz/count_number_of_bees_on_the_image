FROM python:3.7-slim

COPY . /bee_counter

RUN apt-get update -y
RUN apt-get install -y python3-dev build-essential libevent-dev libgtk2.0-dev
RUN pip install -r bee_counter/requirements.txt

WORKDIR /bee_counter

ENTRYPOINT ["python3", "app.py"]
