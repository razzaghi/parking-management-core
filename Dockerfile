FROM python:3.6

WORKDIR /app

COPY . /app/

RUN apt-get update
RUN apt-get install libmariadbclient-dev
#RUN apt-get install libmysqlclient-dev
RUN apt-get install python-pip python-dev libpq-dev
RUN pip install virtualenv
RUN virtualenv env
RUN source env/bin/activate

RUN pip install -r requirements.txt && \
        python manage.py collectstatic --noinput

EXPOSE 8001

CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]