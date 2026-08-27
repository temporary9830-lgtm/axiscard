python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

# Django Settings Path বলে দেওয়া
export DJANGO_SETTINGS_MODULE=newproject.settings

python3 manage.py collectstatic --noinput