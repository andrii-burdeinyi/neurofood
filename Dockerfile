FROM python:3-alpine

MAINTAINER Andrii Burdeinyi <holden1853caulfield@gmail.com>

# Expose the Flask port
EXPOSE 80

WORKDIR /opt/app
# TODO write stuff for crontab running
RUN apk update && apk add py-virtualenv py-mysqldb mariadb-dev build-base mariadb-client-libs

ADD requirements.txt requirements.txt

RUN python3 -m venv venv

RUN . venv/bin/activate && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . .

ENTRYPOINT ["sh"]

CMD ["start.sh"]
