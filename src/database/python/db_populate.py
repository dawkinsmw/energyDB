## Imports
import psycopg2
from psycopg2 import DatabaseError
import requests
import datetime as dt
from src.parser.parser_opennem import parse_request_json
from src.database.python.db_insert_batch import insert_batch


def db_populate(dbc, logger, regions, months):
    for region in regions:
        logger.info(f"starting: {region}")
        for month in months:
            logger.info(f"starting: {month}")
            
            ## URL
            url = f'http://api.opennem.org.au/stats/power/network/fueltech/NEM/{region}?month={month}'

            ## Request data
            logger.debug(f'Requesting {url}..')
            r = requests.get(url)
            r.raise_for_status()

            ## Parse data 
            logger.debug('Parsing JSON..')
            meta, price, power = parse_request_json(r.json())

            ## Insert batch
            logger.debug('Inserting batch..')
            cursor = dbc.cursor()
            insert_batch(cursor,logger,meta,price,power)

            ## Commit transaction
            logger.debug('Commiting to DB..')
            dbc.commit()

