FROM python:3-alpine

MAINTAINER Andrii Burdeinyi <holden1853caulfield@gmail.com>

WORKDIR /opt/app

RUN pip install flask

COPY . .

ENTRYPOINT ["python"]

# Expose the Flask port
EXPOSE 80

CMD ["./web/app.py"]
