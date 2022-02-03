#!/bin/sh

echo "Starting initial setup..."
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --no-input
python manage.py create_generic_user superuser BVT8WnWNF8wJvb4K ezagor@icloud.com --no-input
python manage.py create_generic_user private BVT8WnWNF8wJvb4K ata@4play.com.tr --no-input
echo "Done."
echo "Please change the credentials of generic users using the admin page."
