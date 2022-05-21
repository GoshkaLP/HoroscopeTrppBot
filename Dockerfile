FROM python:3.8.6-buster

WORKDIR /usr/src/app

ADD requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

COPY ./ /usr/src/app/

CMD ["uwsgi", "app.ini"]
