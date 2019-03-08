FROM python:3.6

WORKDIR /app

COPY . /app/

apt-get update
apt-get install libmysqlclient-dev
apt-get install python-pip python-dev libpq-dev
pip install virtualenv
virtualenv env
source env/bin/activate

RUN pip install -r requirements.txt && \
        python manage.py collectstatic --noinput

EXPOSE 8001

CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]