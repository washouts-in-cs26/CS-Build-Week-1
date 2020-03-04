release: python manage.py migrate && python manage.py ./util/create_world.py

web: gunicorn adv_project.wsgi:application --log-file -