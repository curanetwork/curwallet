# Cur wallet #

API server for Cur wallet.

## Quickstart ##

Make sure you have [pipenv installed](https://docs.pipenv.org/install.html). Then install Django 2.0 or later in your virtualenv:

    pip install django>=2.0

Clone this repo

    git clone https://github.com/curanetwork/curwallet-api.git

cd to curwallet-api and install the development dependencies

    pipenv install --dev

If you need a database, edit the settings and create one with
   
    pipenv run python manage.py migrate

Once everything is setup you can run the development server: [http://localhost:8000/](http://localhost:8000/)

    pipenv run python manage.py runserver

Settings are divided by environments: production.py, development.py and testing.py. By default it uses development.py, if you want to change the environment set a environment variable:

    export DJANGO_SETTINGS_MODULE="curwallet.settings.production"

or you can use the `settings` param with runserver:

    pipenv run python manage.py runserver --settings=curwallet.settings.production

If you need to add some settings that are specific for your machine, copy the contents of file `local_example.py` to new file `local_settings.py`. Ensure this file is in .gitignore so the changes won't be tracked.

