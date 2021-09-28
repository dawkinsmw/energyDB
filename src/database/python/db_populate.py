## Imports
import psycopg2
from psycopg2 import DatabaseError
import logging
import requests
import datetime as dt
from src.parser.parser_opennem import parse_request_json
from src.database.python.db_insert_batch import insert_batch
from dateutil.relativedelta import relativedelta

## Config
from conf.database import db_name, db_user, db_pword, db_host, db_port

## Params
from data.names import ZONE_KEY_TO_REGION
regions = ZONE_KEY_TO_REGION.values()
first_month_start = dt.date.fromisoformat('2019-01-01')
final_month_start = dt.date.today().replace(day=1)

## Connect to DB
dbc = psycopg2.connect(user=db_user,
                        password=db_pword,
                        host=db_host,
                        port=db_port,
                        database=db_name)

## Populate DB
for region in regions:
    print(f"starting: {region}")
    while(first_month_start <= final_month_start):
        print(f"    starting: {first_month_start}")
        
        ## URL
        url = f'    http://api.opennem.org.au/stats/power/network/fueltech/NEM/{region}?month={first_month_start}'

        ## Request data
        print(f'    Requesting {url}..')
        r = requests.get(url)
        r.raise_for_status()

        ## Parse data 
        print('    Parsing JSON..')
        meta, price, power = parse_request_json(r.json())

        ## Insert batch
        print('    Inserting batch..')
        cursor = dbc.cursor()
        insert_batch(cursor,logging.getLogger('example_logger'),meta,price,power)

        ## Commit transaction
        print('    Commiting to DB..')
        dbc.commit()

        first_month_start = first_month_start + relativedelta(months=1)

