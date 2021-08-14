# Routers
#### This is a django web app to find registered PSV saccos on relevant routes and their charges

## Description
This is a django web app to find registered PSV saccos on relevant routes and their charges

#### Link to deployed site
None

## Table of content
1. [Description](#description)
2. [Setup and installations](#setup-and-installations)
3. [Production](#Production)

## Setup and installations
* Fork the data onto your own personal repository.
* Clone Project to your machine
* Activate a virtual environment on terminal: `source venv/bin/activate`
* Install all the requirements found in requirements file.
* On your terminal run `python manage.py runserver`
* Access the live site using the local host provided

## Running the tests

To run tests run `python manage.py test`

#### Prerequisites
1. [Python](https://www.python.org/downloads/)
2. [virtualenv](https://virtualenv.pypa.io/en/stable/installation/)
3. [Pip](https://pip.pypa.io/en/stable/installing/)

#### Technologies used
    - Python
    - Django

#### Clone the Repo and rename it to suit your needs.
```bash
https://github.com/JamesMutahi/Routers.git
```
#### Initialize git and add the remote repository
```bash
git init
```
```bash
git remote add origin <your-repository-url>
```

#### Create and activate the virtual environment
```bash
python -m virtualenv venv
```

```bash
source venv/bin/activate
```

#### Setting up environment variables
Create a `.env` file and paste the following filling where appropriate:
```
SECRET_KEY='rdtfyguihjohucbdsjnc'
DEBUG=True
MODE='dev'
```

#### Install dependencies
Install dependencies that will create an environment for the app to run
`pip install -r requirements.txt`

#### Make and run migrations
```bash
python manage.py check
python manage.py makemigrations
python manage.py migrate
```

#### Run the app
```bash
python manage.py runserver
```
Open [localhost:8000](http://127.0.0.1:8000/)

## Production
These constitute setup for production mode.

Change `.env` configuration file to have
```bash
MODE='prod'
DEBUG=False
```