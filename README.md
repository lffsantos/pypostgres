# Installation
[![Build Status](https://travis-ci.org/marcelluzs/pypostgres.svg?branch=master)](https://travis-ci.org/marcelluzs/pypostgres)

```
pip3 install pypostgres
```

*Not tested in python 2.x*

# Basic usage

```python
>>> from pypostgres.postgres import Postgres

# Database connection
'''
    - database      Required
    - user          Required
    - password=''   (default: None)
    - host=''       (default: 127.0.0.1 [localhost])
    - port=''       (default: 5432)
'''
>>> db = Postgres('books', 'john')

## Select query
# Fetch argument can be:
#   'all' or 0 for `fetchall`
#   'one' or 1 for `fetchone`
#   an int for `fetchmany`
>>> db.query('SELECT author FROM books;', fetch='all')
Result(success=True, response=['George R. R. Martin', 'J. R. R. Tolkien'])

## Insert query
>>> values = ('C. S. Lewis', 'The Chronicles of Narnia')
>>> db.query('INSERT INTO books (author, book) VALUES (%s, %s);', values=values)
Result(success=True, response=None)
```


# Connection as `contextmanager`
The Connection class handle the entrance and exit of the database connection, opening the communication when you entered it and closing the cursor/connection when you are out.

```python
>>> from pypostgres.connection import Connection
>>> dsn = 'dbname=books user=john'
>>> with Connection(dsn=dsn) as (connection, cursor):
>>>     # do whatever you want to do
>>>     cursor.execute('SELECT author, book FROM books;')
>>>     data = cursor.fetchone()
>>> data
('C. S. Lewis', 'The Chronicles of Narnia')
```
