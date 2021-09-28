from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def db_destroy(dbc,db_name):
    dbc.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    ## Create new database
    cur = dbc.cursor()
    cur.execute(
        f"DROP DATABASE {db_name};"
    )
