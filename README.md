# Shopee Exercise
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![MySQL](https://img.shields.io/badge/mysql-%2300f.svg?style=for-the-badge&logo=mysql&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

Considering that scenario, build a script, implementing the seller's ranking logic, where the user,
from the terminal, inputs a Sale item and the output is printed as an updated list of all sales
registered, sorted by sellers with the highest to lowest amount sold.

## Requirements
You will need those tools to run the code:

* [Docker](https://www.docker.com/products/docker-desktop/)
* [Docker-Compose](https://docs.docker.com/compose/install/)
* [Python 3.9](https://www.python.org/downloads/)

This exercise was developed with 5 sellers pre-registered in the database, you will need their names to make sales:
1. cloud strife
2. lara croft
3. mario
4. link
5. donkey kong


### 1. Loading environment variables
#### Powershell (Windows)
```
$env:DB_USER = "root"
$env:DB_PASSWORD = "mysecurepass"
$env:DB_HOST = "localhost" 
$env:DB_NAME = "mydb"
```
#### Bash (Linux)
```
export DB_USER=root
export DB_PASSWORD=mysecurepass
export DB_HOST=localhost
export DB_NAME=mydb
```

### 2. Running database
```
docker-compose up -d
```

### 3. Running application
```
pip3 install -r sales_manager/requirements.txt
python3 .\sales_manager\app.py
```

### 4. Running tests
```
python3 -m pytest
```



## Files
```
├───database
├───sales_manager
│   ├───tests
│   ├───app.py
│   ├───helpers.py
│   ├───models.py
│   └───settings.py
└───docker-compose.yaml
```
* `database/*` - Volume folder with all persisent data from db on container.
* `docker-compose.yaml` - File to setup MySQL database.
* `sales_manager/tests/*` - All tests for the application
* `sales_manager/app.py` - Entrypoint for the application
* `sales_manager/helpers.py` - Classes and functions provided to application
* `sales_manager/models.py` - A model is the single, definitive source of information about your data. It contains the essential fields and behaviors of the data you’re storing. Generally, each model maps to a single database table.
* `sales_manager/settings.py` - All settings from enviroment variables

