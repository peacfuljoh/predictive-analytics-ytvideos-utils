
from src.ytpa_utils.sql_utils import make_sql_query, make_sql_query_where_one




def test_make_sql_query():
    tablename = 'table1'
    cols = ['a', 'b', 'c']
    where = dict(a='a', b=[['1', '2']], c=['b', 'c', 'd'])
    limit = 50

    q = make_sql_query(tablename, cols=cols, where=where, limit=limit)
    q = q.replace('  ', ' ')

    q_exp = ("SELECT a,b,c FROM table1 WHERE table1.a = 'a' AND table1.b BETWEEN '1' AND '2' AND table1.c "
             "IN ('b','c','d') LIMIT 50")

    assert q == q_exp


def test_make_sql_query_where_one():
    tablename = 'table1'
    where = dict(a='a', b=[['1', '2']], c=['b', 'c', 'd'])

    q_exp = dict(a=" table1.a = 'a'", b=" table1.b BETWEEN '1' AND '2'", c=" table1.c IN ('b','c','d')")

    for key, val in where.items():
        q = make_sql_query_where_one(tablename, key, val)
        assert q == q_exp[key]

