FROM ubuntu:latest
MAINTAINER Andreas Steffen "andreas.steffen@gmail.com"
RUN apt-get update
RUN apt-get install -y python3-pip python3-dev python3-virtualenv fabric \
      libpq-dev libjpeg-dev libxml2-dev libxslt-dev libfreetype6-dev \
      postgresql-client git curl wget

COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip3 install -r requirements.txt
    
COPY . /app
WORKDIR /app

ENTRYPOINT ["python3"]
CMD ["app.py"]