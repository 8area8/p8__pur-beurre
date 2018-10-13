installation du serveur redis: https://github.com/MicrosoftArchive/redis/releases (msi version)
- à activer depuis le gestionnaire des tâches.
port par défaut: port 6379

- celery pour le management des tasks.
- eventlet pour faire tourner celery sur windows.
- pipenv run celery -A pure_beurre.celery worker --pool=eventlet
- En local, je dois démarrer django et celery. La communication celery est couplé à django.


- créer une première vue.
- configurer reddis en local
- créer une tache redis cliquable
- configurer redis en prod

---

#WEBPACK DJANGO:
https://www.jamesbaltar.com/django-webpack
- pip install django-webpack-loader
- npm install --save-dev webpack webpack-bundle-tracker webpack-cli

- other to see: https://medium.com/uva-mobile-devhub/set-up-react-in-your-django-project-with-webpack-4fe1f8455396

#JQUERY UI
https://openclassrooms.com/fr/courses/510018-decouvrez-la-puissance-de-jquery-ui/510016-lautocompletion
http://flaviusim.com/blog/AJAX-Autocomplete-Search-with-Django-and-jQuery/

#REDIS
http://sametmax.com/files-de-taches-et-taches-recurrentes-avec-celery/
http://docs.celeryproject.org/en/latest/django/first-steps-with-django.html
https://gearheart.io/blog/how-to-deploy-a-django-application-on-heroku/
- celery heroku issue: https://stackoverflow.com/questions/12013220/celery-creating-a-new-connection-for-each-task


#slugignore
https://devcenter.heroku.com/articles/slug-compiler#ignoring-files-with-
--------

- pipfile et pipfile.lock = pipenv
- package-lock.json + package.json + webpack-stats.json + webpack.conf.js = npm webpack
- node_modules = npm

- pure_beurre + django_apps = django


---
JS ANIMATION: https://github.com/legomushroom/mojs

JS PACKAGES:

-scroll reveal (ScrollReveal({reset: true}).reveal('.headline');)
https://scrollrevealjs.org/guide/customization.html, https://github.com/scrollreveal/scrollreveal

webpack config output property, for django_webpack statics:
- publicPath: '/static/bundles/'

-----

How I configured my local_setting.py :
```python
def settings(config):
    """Modify the base configuration."""
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
```

----
4 serveurs à lancer:
- l'app django
- le serveur postgres
- le serveur redis
- le serveur celery


CREDITS

Photo by Olenka Kotyk on Unsplash
Carrot by Fabien Jouin from the Noun Project

ICONS

https://material.io/tools/icons/?icon=exit_to_app&style=twotone
- <i class="material-icons-new icon-white twotone-account_circle"></i>