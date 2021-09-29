## Imports
import psycopg2
import logging
import logging.config
import datetime as dt
from src.database.python.db_create import db_create
from src.database.python.db_destroy import db_destroy
from src.database.python.db_up import db_up
from src.database.python.db_down import db_down
from src.database.python.db_populate import db_populate

## Config
from conf.database import db_name, db_user, db_pword, db_host, db_port
logging.config.fileConfig(fname='conf/logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)

## Params
regions = ['NSW1',"SA1"]
months = [
    dt.date.fromisoformat('2021-07-01'),
    dt.date.fromisoformat('2021-08-01')
    ]

## Connect to DB
dbc = psycopg2.connect(user=db_user,
                        password=db_pword,
                        host=db_host,
                        port=db_port,
                        database=db_name)
db_down(dbc)
db_up(dbc,logger)
db_populate(dbc,logger,regions, months)
dbc.close()

