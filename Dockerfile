FROM python:3.8

COPY . /api_test
WORKDIR /api_test
RUN apt-get update -y
RUN pip install -r requirements.txt
# CMD ["uwsgi", "--ini api_test/uwsgi.ini"]
# CMD ["python", "manage.py runserver 0.0.0.0:8000"]
