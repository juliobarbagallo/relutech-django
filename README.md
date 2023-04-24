# ACME
This is a Django application to handle resources management by RESTful API.

## Features
User authentication: It protect endpoint using Token.
Developers: This model handle the developers of the company and allows CRUD actions at /api/developers.
Assets: This model handle the assets of the company and allows CRUD actions at /api/developers.
Licenses: This model handle the licenses of the company and allows CRUD actions at /api/developers.


## Technologies Used
Django framework.
sqlite.
Docker.
Swagger.

## Setup and Installation
pipenv should be installed and we assume docker is installed and running.
- Check docker is installed and running.
```bash
 dcoker ps
```

- Install pipenv
```bash
 pip install pipenv
```

- Clone the project.

```bash
git clone https://github.com/juliobarbagallo/relutech-django.git
```
- Go to the new created directory.

```bash
cd relutech-django
```
- Install dependencies and activate environment.

```bash
pipenv install
pipenv shell
```
- Run using Docker.

```bash
docker-compose up --build
```

- Now you can use the browser no navigate to: http://127.0.0.1:8000/swagger/ and see the endpoints documentation
- And use POSTMAN to perform CRUD operations in order to handle the company resource.


  
Usage
Endpoinst are protected, only superusers can perfomr CRUD operations and also the request body needs to send Token.