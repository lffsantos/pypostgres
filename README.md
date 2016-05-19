# Installation

```
pip install pypostgres
```

# Usage

```python
>>> from pypostgres import Postgres

# Database connection
>>> db = Postgres('dbname', 'user')

# Execute query
>>> db.query('SELECT * FROM dbname;', mode='read')
>>> [(1, 99, "def'abc"), (2, 100, "abc'def")]

# Insert query
>>> db.query('INSERT INTO dbname (a, b) VALUES (%s, %s);', (1, 2), mode='write')
# return None

# DataFrame query
>>> db.to_dataframe(['id', 'num', 'data'], 'dbname', conditions="num > 1")
>>> 
    id    num       data
0  2.0  100.0  "abc'def"

# Inserting a DataFrame
>>> import pandas as pd
>>> df = pd.DataFrame([(3, 98, 'test')], columns=['id', 'num', 'data'])
>>> db.from_dataframe(df, 'dbname')
# return None
```