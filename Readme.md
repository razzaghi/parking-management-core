## How to launch application

(I think python, pip installed)

### install OS (Ubuntu) requirements
    * apt-get install mysql-server
    * apt-get install libmysqlclient-dev
    * apt-get install python-pip python-dev libpq-dev postgresql postgresql-contrib nginx
    * pip install virtualenv

### Install launch dependency in root of project
* virtualenv env
* source env/bin/activate
* pip install -r requirements.txt
* cp .env.template .env
* create datebase in mysql
* config mysql configuration in .env file
* python manage.py migrate
* python manage.py createsuperuser
* python managet.py runserver

## Define data
* Login with created user
* Define ParkingTypes (Car, MotorCycle)
* Define Parkings
* Add In/Out in ParkingInOut
* After add In/Out you can check AvailavleSpace in Parkings is update