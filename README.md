# Usage

```python
from postgres import Postgres

# Database connection
db = Postgres('dbname', 'user')

# Select query
db.read('SELECT * FROM test;')
# return a list of tuples

# Insert query
db.write('INSERT INTO test (a, b) VALUES (%s, %s);', (1, 2))
# return None
```