
# Pur Beurre application

![version](https://img.shields.io/badge/version-1.1-blue.svg?longCache=true&style=flat-square) ![version](https://img.shields.io/badge/python-3.6-ligh.svg?longCache=true&style=flat-square) ![version](https://img.shields.io/badge/project-web_app-orange.svg?longCache=true&style=flat-square)

## News

- 06/11/2018 : release **1.1** done. The substitute save button is disabled if the user already has it.
- 06/11/2018 : release **1.0** done. All features are implemented.  

## Presentation

![Pur Beurre app example](https://i.imgur.com/cnvOiDb.jpg)

This project is an application that allows to find healthier substitutes for each food. The user can then save the substitutes of his choice. The project uses the OpenFoodFact API.

## Specificities

- an advanced search system, with autocompletion
- a login system, especially with google
- the ability to save his substitutes
- A strong administration page
- Using Celery, and Redis as a cache server
- Using webpack to manage the static files

## Getting Started

You can clone this repository to your local drive and then deploy it to heroku.

### Prerequisites

to use it, you'll need to install:

- python 3.6
- pipenv
- Redis (for local testing)
- PostgreSQL (for local testing)

### Installing

Run pipenv at the root of the repository to install dependencies.

### Local testing

You'll have to create a local_settings file if you want to run the application on local. Google_settings file is also required for local and production.  
You need to get a key and secret pass from "google developers" for local and production environments.
Finally, use this command to run the celery server:
```celery -A app.celery worker --pool=eventlet```. Eventled fixes a windows bug.

#### Settings configurations

```python
"""My local_settings.py."""


def settings(config):
    """Local settings."""
    config["DEBUG"] = True
    config["TEMPLATE_DEBUG"] = True

    config["DATABASES"] = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'your_database_name',
            'USER': "postgres",
            'PASSWORD': 'your_password',
            'HOST': '127.0.0.1',
            'PORT': '5432'
        }
    }

    config["CELERY_BROKER_URL"] = 'redis://localhost:6379/0'
    config["CELERY_RESULT_BACKEND"] = 'redis://localhost:6379/0'
    config["SOCIAL_AUTH_GOOGLE_OAUTH2_KEY"] = "xxxxxxxxx"
    config["SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET"] = "xxxxxxxxx"

```

## Running the tests

Simply write ```pipenv run python manage.py test``` in your shell, at the root of this repository.

## Deployment

Use heroku for deployment.  
You have to create a heroku account and set this project to a new heroku project. You must activate the Redis addon. Then simply write ```git push heroku master``` to deploy your application.  
Create two environment variables on your Heroku dashboard, and call them "GOOGLE_KEY" for the key, and "GOOGLE_PASS" for the password.  

## Built With

### Core dev

- python - back language.  
- npm, webpack - Front-end developement.  
- Bootstrap 4 - css/js framework.  
- Jquery - Javascript framework.
- Scroll-reveal - Javascript package for animated scrolling.
- Jquery UI autocomplete - Jquery package for autocompletion.  
- Django - python web framework.  
- Django-social-auth - Django package for social authenticates (ex: google)
- Django-webpack - Django package for a nice implementation of webpack to django.
- Django-heroku - Django package for a nice implementation of Django to heroku.
- requests - nice python requests package.

### Third API

- OpenFoodFact API

## Trello Scrum project

**Link to Trello:**
[![link to Trello](https://i.imgur.com/JrioLlb.jpg)](https://trello.com/p8_pure_beurre)

## Authors

Mikael Briolet - Initial work - OpenClassroom

Photo by Olenka Kotyk on Unsplash - background index  
Photo by Annie Spratt on Unsplash - background account  
Photo by Brooke Lark on Unsplash - signup  
Photo by Jay Wennington on Unsplash - results_list  
Photo by Christine Siracusa on Unsplash - substitutes  
Photo by Harry Brewer on Unsplash - mentions  
Carrot by Fabien Jouin from the Noun Project  

## License

MIT license.