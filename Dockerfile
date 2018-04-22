FROM python:3-alpine

MAINTAINER Andrii Burdeinyi <holden1853caulfield@gmail.com>

# Expose the Flask port
EXPOSE 80

WORKDIR /opt/app

RUN apk update && apk add py-virtualenv

COPY . .

# Installing python environment
RUN  pip install --upgrade pip && \
     pip install -r requirements.txt

ENTRYPOINT ["python"]

CMD ["./web/app.py"]
