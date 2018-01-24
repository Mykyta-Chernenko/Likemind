FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN mkdir /backend
WORKDIR /backend
ADD requirements.txt /backend/
RUN apt-get update && apt-get install -y redis-server
RUN pip install Django==2.0.1
RUN pip install djangorestframework==3.7.7
RUN pip install cryptography==2.1.4
RUN pip install coreapi==2.3.3
RUN pip install channels
RUN pip install asgi_redis==1.4.3
EXPOSE 6379
CMD ["/usr/bin/redis-server"]
