user = 'root'
password = 'mysecurepass'
database_name = 'mydb'
# database_host = 'mysql_db'
database_host = 'localhost'

db_conn_str = f"mysql://{user}:{password}@{database_host}/{database_name}"
