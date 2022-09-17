import os

db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_name = os.getenv('DB_NAME')

db_conn_str = f"mysql://{db_user}:{db_password}@{db_host}/{db_name}"
