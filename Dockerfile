FROM python:3-alpine

MAINTAINER Andrii Burdeinyi <holden1853caulfield@gmail.com>

# Expose the Flask port
EXPOSE 80

WORKDIR /opt/app

RUN apk update && apk add py-virtualenv

ADD requirements.txt requirements.txt

# Installing python environment
RUN  pip install --upgrade pip && \
     pip install -r requirements.txt

COPY . .

ENTRYPOINT ["python"]

CMD ["./run.py"]
