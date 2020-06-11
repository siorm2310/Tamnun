# Tamnun

## תמנו"ן - תכנון משימה נוח ונגיש

Web - based flight configuration calculator for the IAF.
Django web application with custom API
Frontend based on vanilla JavaScript

## Prerequisites

- python version 3.7 or higher
- packages listed in the requirements.txt

## Installation

1. Install python
2. Set up a virtual environment by running the command `python -m venv django_venv`
3. Install packages by running `pip install -r requirements.txt`
4. Set up PosgreSQL server (either by installing or setting up a container)
5. Use the settings.py to configure the DB.
6. run the command `python manage.py makemigrations` and `python manage.py migrate` to sync the DB with Django
