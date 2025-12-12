set -o errexit

pip install -r requirements.text

python manage.py migrate