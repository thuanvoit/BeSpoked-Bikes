# BeSpoked-Bikes

BeSpoked Bikes' sale tracking application.

## Getting Started

### Technologies
* Python
* Django
* HTML, CSS, JS
* REST API
* Bootstrap
* SQLite3 (Development)
* Postgres (Deployment)
* Github

### Deployment

Deployment branch `deploy`

* Microsoft Azure

### Must known before using

* Sample on the application is for demo. It would take a while to seed a huge amount of sample data. Message when finish "Feed data successfully."

### Install dependencies

``` bash
pip install -r requirements.txt
```

### On Cloud (PostgresSQL)

[https://bespoked-bikes.azurewebsites.net/](https://bespoked-bikes.azurewebsites.net/)

### Run Locally (SQLite3)

Switch to branch `local_test`

### Migration

``` bash
python manage.py makemigrations
python manage.py migrate
```

Run the app:

``` bash
python manage.py runserver
```