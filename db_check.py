import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "car_rental_app.settings")
django.setup()

from django.db import connection

with connection.cursor() as cursor:
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Tables in the database:")
    print(tables)
