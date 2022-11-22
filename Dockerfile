# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /final_project

COPY requirements.txt requirements.txt

RUN apt-get update && apt-get upgrade

RUN apt-get -y install gcc 

RUN apt-get -y install libxml2-dev libxslt1-dev zlib1g-dev g++

RUN python3 -m pip install --upgrade pip

RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]