set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate
python manage.py create_doctoruser

#python manage.py create_superuser
#python manage.py assign_permissions
#python manage.py import_cie10 apps/service_end/data/cie10_codes.xlsx