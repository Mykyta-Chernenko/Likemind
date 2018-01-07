FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN mkdir /backend
WORKDIR /backend
ADD requirements.txt /backend/
RUN pip install Django==1.11.1
RUN pip install djangorestframework==3.5.4
RUN pip install django-rest-swagger==2.1.2
RUN pip install cryptography==2.1.4

#ADD . /backend/
