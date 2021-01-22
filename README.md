# Specialist service
Specialist search service with message chat and geolocation, developed using Django. 
That service can be used by both specialist for posting resume and by ordinary users
to find an appropriate employee.

## Frameworks and packages
* Django - framework for web-application development
* Geopy - python client for geocoding services
* Django channels - project that can handle WebSocket, chat protocols, IoT protocols
and more in Django

## Databases
For this project i'm using MySql to store models. For working with it i use django ORM.

## Installation
1. Clone repository (dev branch)
2. Change directory to project folder
3. Build images with docker-compose `docker-compose build`
4. Run django migrations `docker-compose run web python manage.py migrate`
5. If you want to create admin for using django panel (CRUD operations) 
`docker-compose run web python manage.py createsuperuser` and then input admin username,
email, password
6. To run server `docker-compose up`, to run in background `docker-compose up -d`
7. Finally application will be started on http://127.0.0.1:8001/

## Tests
Tests are run by django `docker-compose web run python manage.py test`
