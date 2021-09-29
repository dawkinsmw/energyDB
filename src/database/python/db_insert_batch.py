## Codes
from data.names import ZONE_KEY_TO_REGION, REGION_LONG_NAMES, NETWORK_LONG_NAMES
REGION_TO_ZONE_KEY = {value:key for key, value in ZONE_KEY_TO_REGION.items()}

## Helpers
def power_attribute_check(attribute,power):
    power_attributes = [power[pk]["meta"][attribute] for pk in power.keys()]
    if all(x == power_attributes[0] for x in power_attributes):
        return power_attributes[0]

## Insert batch
def insert_batch(cursor,logger,meta,price,power):

    ## DIM_NETWORK
    logger.debug('insert_batch: DIM_NETWORK')
    # data
    network = meta["network"].upper()
    # check if already exists
    cursor.execute(
        f"select id from Dim_Network where code = '{network}'"
    )
    network_index = cursor.fetchone()
    # if not insert as new entry
    if(network_index is None):
        cursor.execute(
            f"INSERT INTO Dim_Network(code) VALUES ('{network}') RETURNING id"
        )
        network_index = cursor.fetchone()
        logger.debug(f'new network: {network_index[0]}, {network}')
    network_index = network_index[0]

    ## DIM_REGION
    logger.debug('insert_batch: DIM_REGION')
    # data
    region_code = meta["code"].upper()
    region_zone = REGION_TO_ZONE_KEY[region_code]
    region_shortname = meta["region"].upper()
    region_longname = REGION_LONG_NAMES[region_code]
    # check if already exists
    cursor.execute(
        f"select id from Dim_Region where code = '{region_code}'"
    )
    region_index = cursor.fetchone()
    # if not insert as new entry
    if(region_index is None):
        cursor.execute(
        f"INSERT INTO Dim_Region(code, short_name) VALUES ('{region_code}', '{region_shortname}') RETURNING id"
        )
        region_index = cursor.fetchone()
        logger.debug(f'new region: {region_index[0]}, {region_code}')
    region_index = region_index[0]

    ## DIM_FUELTECH
    logger.debug('insert_batch: DIM_FUELTECH')
    ft_indexes = {}
    for ft in power.keys():
        # check if already exists
        cursor.execute(
            f"select id from Dim_Fueltech where long_name = '{ft}'"
        )
        ft_index = cursor.fetchone()
        # if not insert as new entry
        if(ft_index is None):
            cursor.execute(
                f"INSERT INTO Dim_Fueltech(long_name) VALUES ('{ft}') RETURNING id"
            )
            ft_index = cursor.fetchone()
            logger.debug(f'new fueltech: {ft_index[0]}, {ft}')
        ft_indexes[ft] = ft_index[0]

    ## DIM_BATCH
    logger.debug('insert_batch: DIM_BATCH')
    # data
    try:
        # network_code = network_index
        # region_code = region_index
        month_start = price['meta']['start']
        api_version = meta["version"]
        pull_date = meta["created_at"]
        price_interval = price['meta']['interval']
        price_units = price['meta']["units"]
        power_interval = power_attribute_check('interval',power)
        power_units = power_attribute_check("units",power)
        # insert
        cursor.execute(
            f"INSERT INTO Dim_Batch(network_id, region_id, month_start, api_version, pull_date, price_interval, power_interval, price_units, power_units) VALUES ('{network_index}', '{region_index}', '{month_start}', '{api_version}', '{pull_date}', '{price_interval}', '{power_interval}', '{price_units}', '{power_units}') RETURNING id"
        )
        batch_index = cursor.fetchone()[0]
        logger.debug(f'new batch: {batch_index}')
    except Exception as e:
        logger.error(f"Batch {batch_index} failed")
        logger.error(f"failed to insert ('{network_index}', '{region_index}', '{month_start}', '{api_version}', '{pull_date}', '{price_interval}', '{power_interval}', '{price_units}', '{power_units}') into Dim_Batch")
        logger.error(e)

    ## FACT_POWER
    logger.debug('insert_batch: FACT_POWER')
    for ft in power.keys():
        for ts, pw in power[ft]['data']:
            try:
                if(pw is None):
                    cursor.execute(
                        f"INSERT INTO Fact_Power(batch_id,interval_start,fueltech_id) VALUES ('{batch_index}', '{ts}', '{ft_indexes[ft]}')"
                    )
                else:
                    cursor.execute(
                        f"INSERT INTO Fact_Power(batch_id,interval_start,fueltech_id,power) VALUES ('{batch_index}', '{ts}', '{ft_indexes[ft]}', '{pw}')"
                    )
            except Exception as e:
                logger.error(f"Batch {batch_index} failed")
                logger.error(f"failed to insert ('{batch_index}', '{ts}', '{ft_indexes[ft]}', '{pw}') into Fact_Power")
                logger.error(e)

    ## FACT_PRICE
    logger.debug('insert_batch: FACT_PRICE')
    for ts, pc in price['data']:
        try:
            if(pc is None):
                cursor.execute(
                f"INSERT INTO Fact_Price(batch_id,interval_start) VALUES ('{batch_index}', '{ts}')"
                )
            else:
                cursor.execute(
                    f"INSERT INTO Fact_Price(batch_id,interval_start,price) VALUES ('{batch_index}', '{ts}', '{pc}')"
                )
        except Exception as e:
            logger.error(f"Batch {batch_index} failed")
            logger.error(f"failed to insert ('{batch_index}', '{ts}', '{pc}') into Fact_Price")
            logger.error(e)

    ## FACT_X_CAP
    logger.debug('insert_batch: FACT_X_CAP')
    for ft in power.keys():
        try:
            cursor.execute(
                f"INSERT INTO Fact_X_Cap(batch_id,fueltech_id,x_capacity) VALUES ('{batch_index}', '{ft_indexes[ft]}', '{power[ft]['meta']['x_capacity_at_present']}')"
            )
        except Exception as e:
            logger.error(f"Batch {batch_index} failed")
            logger.error(f"failed to insert ('{batch_index}', '{ft_indexes[ft]}', '{power[ft]['meta']['x_capacity_at_present']}') into Fact_X_Cap")
            logger.error(e)

