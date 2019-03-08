FROM python:3.6

WORKDIR /app

COPY . /app/

RUN apt-get -y update
RUN apt-get install -y mysql-server
RUN apt-get install -y libmysqlclient-dev
RUN pip install virtualenv
RUN virtualenv env
RUN chmod 777 ./env -Rf
RUN ./env/bin/activate

RUN pip install -r requirements.txt

EXPOSE 8001

CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]