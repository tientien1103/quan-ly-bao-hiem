from django.apps import AppConfig
from django.db import connections
from django.db.utils import OperationalError
import sys

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        if 'runserver' not in sys.argv:
            return True
            
        try:
            db_conn = connections['default']
            db_conn.cursor()
            print("\n=================================")
            print("Connected to SQLite database successfully!")
            print("=================================")
            print(f"Server is running!")
            print("API Documentation: http://localhost:8000/api/docs/")
            print("Admin interface: http://localhost:8000/admin/")
            print("=================================\n")
        except OperationalError:
            print("\n=================================")
            print("Database connection failed!")
            print("=================================\n")
            raise 