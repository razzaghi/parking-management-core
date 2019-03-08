FROM python:2.7

WORKDIR /app

COPY . /app/

RUN apt-get -y update
#RUN apt-get install libmariadbclient-dev
RUN apt-get install -y default-libmysqlclient-dev
RUN pip install virtualenv
#RUN pip install mysql-python
RUN virtualenv env
#RUN source env/bin/activate

RUN pip install -r requirements.txt && \
        python manage.py collectstatic --noinput

EXPOSE 8001

CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]