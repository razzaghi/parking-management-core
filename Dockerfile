FROM python:3.6-slim-jessie

WORKDIR /app

COPY . /app/

RUN apt-get -y update
RUN apt-get install -y python-pip python-dev libpq-dev
RUN apt-get install -y libmysqlclient-dev
RUN pip install --upgrade setuptools
RUN pip install virtualenv
RUN virtualenv env
RUN chmod 777 ./env -Rf
RUN ./env/bin/activate

RUN pip install -r requirements.txt

EXPOSE 8001

CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]