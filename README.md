# Installation
[![Build Status](https://travis-ci.org/marcelluzs/pypostgres.svg?branch=master)](https://travis-ci.org/marcelluzs/pypostgres)

```
pip3 install pypostgres
```

*Not tested in python 2.x*

# Basic usage
Just connect to your db using Postgres class and pass the queries to `.query()` method. 
The `.query()` method will return a custom `Cursor` class, if you don't want nothing back from the db, you don't need to store it but if you want to fetch any data, you can do it whenever you want because the `Cursor` class will always handle the real connection with the db. In other words you will never need to worry about closed cursors or connections because only at the exact time you request data from db the `Cursor` class opens the connection and then it closes it.

```python
>>> from pypostgres.postgres import Postgres

# Database connection
# http://initd.org/psycopg/docs/module.html#psycopg2.connect
>>> db = Postgres(database='books', user='john')
>>> cursor = db.query('SELECT author FROM books;')
>>> cursor.one
('George R. R. Martin',)
>>> cursor.all
[('George R. R. Martin',), ('J. R. R. Tolkien',)]
```

# Postgres class
1. `mogrify`: [psycopg2.cursor.mogrify()](http://initd.org/psycopg/docs/cursor.html#cursor.mogrify "cursor.mogrify()")
2. `query`: return `Cursor` object for given `sql` statements and (optional) `values`
3. `get_columns`: return `table` columns
4. `get_tables`: return all tables in current db
5. `get_databases`: return all dbs in current connectino

# Cursor class
If you are *SELECTing* data, the `Cursor` object can help you *fetch* that data. You have two options:

## Properties

1. `Cursor.one`: return one result
2. `Cursor.all`: return all results
3. `Cursor.many(n)` (actually a method): return `n` results

## Fetch method
Just pass how many result you want e.g. `.fetch(n)`:

1. `1` or `one` for one
2. `0`, `*` or `all` for all
3. An *int* for other values

# Connection class as `contextmanager`
The Connection class handle the entrance and exit of the database connection, opening the communication when you entered it and closing the connection when you are out.

```python
>>> from pypostgres.connection import Connection
>>> dsn = 'dbname=books user=john'
>>> with Connection(dsn=dsn) as conn:
>>>     # do whatever you want to do
>>>     cursor = conn.cursor()
>>>     cursor.execute('SELECT author, book FROM books;')
>>>     data = cursor.fetchone()
>>> data
('C. S. Lewis', 'The Chronicles of Narnia')
```
