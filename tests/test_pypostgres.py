import psycopg2
import pytest
import testing.postgresql

from pypostgres.postgres import Postgres


def create_database(cursor):
    cursor.execute(
        'CREATE TABLE test (id INTEGER , message varchar(3000), PRIMARY KEY (id));'
    )


@pytest.fixture
def fake_database():
    with testing.postgresql.Postgresql() as postgresql:
        db = psycopg2.connect(**postgresql.dsn())
        cur = db.cursor()
        create_database(cur)
        db.commit()
        yield postgresql.dsn()

        db.close()


def test_insert_one_without_fetch(fake_database):
    db = Postgres(**fake_database)
    cursor = db.query(
        "insert into test (id, message) values (1, 'test_message')"
    )
    pk = cursor.commit()
    assert not pk
    query_test = db.query("select count(*) from test")
    assert len(query_test.all) == 1


def test_insert_one_with_fetch(fake_database):
    db = Postgres(**fake_database)
    cursor = db.query(
        "insert into test (id, message) values (1, 'test_message') returning id")
    pk = cursor.commit(fetch=True)
    assert pk[0] == 1


@pytest.mark.parametrize('values, expected_count ', [
    [[(i,  'insert '+ str(i))for i in range(1, 4)], 3],
    [[(i, 'insert '+ str(i)) for i in range(1, 6)], 5],
])
def test_insert_bulk(fake_database, values, expected_count):
    db = Postgres(**fake_database)
    sql = 'insert into test (id, message) values (%s, %s)'
    cursor = db.query(sql=sql, values=values)
    cursor.commit()
    query_test = db.query("select count(*) from test")
    assert query_test.one[0] == expected_count


@pytest.mark.parametrize('values, return_id', [
    [[(i,  'insert '+ str(i))for i in range(1, 4)], 1],
    [[(i,  'insert '+ str(i))for i in range(1, 10)], 5],
])
def test_select_one(fake_database, values, return_id):
    db = Postgres(**fake_database)
    sql = 'insert into test (id, message) values (%s, %s)'
    cursor = db.query(sql=sql, values=values)
    cursor.commit()
    query_test = db.query(sql="select * from test where id=%s", values=(return_id, ))
    result = query_test.one
    assert result == (values[return_id-1])


@pytest.mark.parametrize('values', [
    [(i,  'insert '+ str(i))for i in range(1, 4)],
    [(i,  'insert '+ str(i))for i in range(1, 10)],
])
def test_select_all(fake_database, values):
    db = Postgres(**fake_database)
    sql = 'insert into test (id, message) values (%s, %s)'
    cursor = db.query(sql=sql, values=values)
    cursor.commit()
    query_test = db.query(sql="select * from test")
    assert query_test.all == values
