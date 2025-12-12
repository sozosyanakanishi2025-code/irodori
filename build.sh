set -o errexit

pip install -r requirements.txt

python manage.py migrate

if [[ -n "$DJANGO_SUPERUSER_USERNAME" ]]; then
    echo "Creating superuser..."
    python manage.py createsuperuser --noinput || echo "Superuser already exists."
fi