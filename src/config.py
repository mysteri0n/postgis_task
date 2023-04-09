import os

DB_HOST = os.getenv('DB_HOST', "postgis")
DB_NAME = os.getenv('DB_NAME', "postgis")
DB_USER = os.getenv('DB_USER', "postgres")
DB_PASSWORD = os.getenv('DB_PASSWORD', "pwd")
