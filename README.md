# create table
```bash
mysql -u root -p
mysql> create database <your_db_name>;
Query OK, 1 row affected (0.01 sec)
```

#Add environment variable
```bash
export FLASK_APP=${PWD}/app.py
```

# initial database
```bash
flask db init
flask db migrate
flask db upgrade
flask initdb
```

# run app
flask run -p 8888


