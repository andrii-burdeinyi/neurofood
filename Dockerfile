FROM python:3-alpine

MAINTAINER Andrii Burdeinyi <holden1853caulfield@gmail.com>

WORKDIR /opt/app
# TODO write stuff for crontab running
RUN apk update
RUN apk add linux-headers \
            build-base \
            openrc

# Supervisord
RUN apk add --no-cache supervisor
COPY docker/supervisor/supervisord.ini /etc/supervisor.d/supervisord.ini

# UWSGI
RUN mkdir -p /var/log/uwsgi
ADD docker/uwsgi/uwsgi.conf /etc/init
COPY docker/uwsgi/neurofood_uwsgi.ini /etc/uwsgi/uwsgi.ini

# PYTHON LIBS
ADD requirements.txt requirements.txt
RUN  pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . .

RUN ["chmod", "+x", "/opt/app/entrypoint.sh"]
ENTRYPOINT ["sh", "/opt/app/entrypoint.sh"]