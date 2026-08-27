python3 -m pip install -r requirements.txt
python3 manage.py collectstatic --noinput
#!/bin/bash
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate --noinput