from django.apps import AppConfig
from django.db import connection
import sys


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"

    def ready(self):
        try:
            connection.ensure_connection()
            print("Database connected")
        except Exception as e:
            print("Database connection failed")
            print(e)

            sys.exit(1)