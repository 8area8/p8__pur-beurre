from collections import Counter

from celery import Celery

# Configuration de celery. Ceci peut aussi se faire dans un fichier de config.
# Ici on dit à celery que pour le module 'tasks', on va utiliser redis
# comme broker (passeur de massage) et comme result backend (stockage du
# resultat des tâches).
celery = Celery('tasks', broker='redis://localhost:6379/0',
                backend='redis://localhost:6379/0')


# Et voici notre première tâche. C'est une fonction Python normale, décorée
# avec un decorateur de celery. Elle prend une URL, et calcule le nombre
# de lettre "e" qu'il y a dans la page.
@celery.task
def ecount():
    print("worked")
