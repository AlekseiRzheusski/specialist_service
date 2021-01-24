FROM python:3.8.6

ENV PYTHONUNBUFFERED 1

RUN mkdir /base
WORKDIR /base
ADD requirements.txt /base/
RUN pip install -r requirements.txt