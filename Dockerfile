FROM python:3

RUN apt-get update
RUN pip install --upgrade pip
RUN pip install requests discord os