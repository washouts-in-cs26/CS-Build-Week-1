<<<<<<< HEAD
python manage.py migrate && python manage.py loaddata ./fixtures/world-generate.json
=======
release: python manage.py migrate && python manage.py ./util/create_world.py
>>>>>>> 0a63f1288ac1bbd2eceaa42d708300b75ca18c12

web: gunicorn adv_project.wsgi:application --log-file -