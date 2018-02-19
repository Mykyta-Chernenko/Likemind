FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN mkdir /backend
WORKDIR /backend
#ADD requirements.txt /backend/
RUN pip install Django==2.0.2
RUN pip install djangorestframework==3.7.7
RUN pip install cryptography==2.1.4
RUN pip install coreapi==2.3.3
RUN pip install psycopg2==2.6
RUN pip install redis==2.10.6
RUN pip install djangorestframework-jwt==1.11
RUN pip install django-cors-headers==2.1.0
RUN pip install djangorestframework-queryfields==1.0.0
RUN pip install django-audiofield
RUN pip install Pillow
RUN pip install django-phonenumber-field
RUN pip install channels
RUN pip install channels_redis
