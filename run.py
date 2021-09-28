## Imports
import psycopg2
from src.database.python.db_create import db_create
from src.database.python.db_destroy import db_destroy
from src.database.python.db_up import db_up
from src.database.python.db_down import db_down
from src.database.python.db_populate import db_populate

## Config
from conf.database import db_name, db_user, db_pword, db_host, db_port

## Connect to DB
dbc = psycopg2.connect(user=db_user,
                        password=db_pword,
                        host=db_host,
                        port=db_port,
                        database=db_name)
db_populate(dbc)
dbc.close()