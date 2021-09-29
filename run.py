## Imports
import psycopg2
import logging
import logging.config
import datetime as dt
from dateutil.relativedelta import relativedelta
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
regions = ['NSW1',"SA1",'QLD1','TAS1','VIC1','WEM']
final_month_start = dt.date.today().replace(day=1)
months = [final_month_start - relativedelta(months=i) for i in range(24)]

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

