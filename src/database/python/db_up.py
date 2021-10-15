
def db_up(dbc,logger):
    cur = dbc.cursor()

    logger.debug("db_up: Dim_Fueltech")
    cur.execute(
    f"create table Dim_Fueltech (\
            id serial PRIMARY KEY,\
            long_name  varchar(50) UNIQUE\
    );"
    )

    logger.debug("db_up: Dim_Network")
    cur.execute(
    f"create table Dim_Network (\
            id  serial PRIMARY KEY,\
            code  varchar(10) UNIQUE,\
            long_name varchar(50)\
    );"
    )

    logger.debug("db_up: Dim_Region")
    cur.execute(
    f"create table Dim_Region (\
            id serial PRIMARY KEY,\
            code  varchar(10) UNIQUE,\
            zone varchar(10) UNIQUE,\
            short_name varchar(10),\
            long_name varchar(50)\
    );"
    )
        
    logger.debug("db_up: Dim_Batch")
    cur.execute(
    f"create table Dim_Batch (\
            id  serial PRIMARY KEY,\
            network_id  integer,\
            region_id  integer,\
            month_start  date,\
            api_version  varchar(11),\
            pull_date  timestamp with time zone UNIQUE,\
            price_interval interval,\
            power_interval interval,\
            price_units  varchar(10),\
            power_units  varchar(10),\
        CONSTRAINT fk_network\
            FOREIGN KEY(network_id) \
            REFERENCES Dim_Network(id),\
        CONSTRAINT fk_region\
            FOREIGN KEY(region_id) \
            REFERENCES Dim_Region(id)\
    );"
    )

    logger.debug("db_up: Fact_Power")
    cur.execute(
    f"create table Fact_Power (\
            batch_id integer,\
            interval_start  timestamp,\
            fueltech_id  integer,\
            power  float,\
        CONSTRAINT pk_power\
            PRIMARY KEY(batch_id, interval_start, fueltech_id),\
        CONSTRAINT fk_batch\
            FOREIGN KEY(batch_id) \
            REFERENCES Dim_Batch(id),\
        CONSTRAINT fk_fueltech\
            FOREIGN KEY(fueltech_id) \
            REFERENCES Dim_Fueltech(id)\
    );"
    )

    logger.debug("db_up: Fact_Price")
    cur.execute(
    f"create table Fact_Price (\
            batch_id integer,\
            interval_start  timestamp,\
            price  money,\
        CONSTRAINT pk_price\
            PRIMARY KEY(batch_id, interval_start),\
        CONSTRAINT fk_batch\
            FOREIGN KEY(batch_id) \
            REFERENCES Dim_Batch(id)\
    );"
    )

    logger.debug("db_up: Fact_X_Cap")
    cur.execute(
    f"create table Fact_X_Cap (\
            batch_id  integer,\
            fueltech_id  integer,\
            x_capacity  float,\
        CONSTRAINT pk_x_cap\
            PRIMARY KEY(batch_id, fueltech_id),\
        CONSTRAINT fk_batch\
            FOREIGN KEY(batch_id) \
            REFERENCES Dim_Batch(id),\
        CONSTRAINT fk_fueltech\
            FOREIGN KEY(fueltech_id) \
            REFERENCES Dim_Fueltech(id)\
    );"
    )
    
    logger.debug("db_up: Fact_CarbonFactor")
    cur.execute(
    f"create table Fact_CarbonFactor (\
            network_id integer,\
            region_id integer,\
            fueltech_id integer,\
            carbon_factor numeric,\
        CONSTRAINT pk_carbonfactor\
            PRIMARY KEY(network_id, region_id, fueltech_id),\
        CONSTRAINT fk_batch\
            FOREIGN KEY(network_id) \
            REFERENCES Dim_Network(id),\
        CONSTRAINT fk_batch\
            FOREIGN KEY(region_id) \
            REFERENCES Dim_Region(id),\
        CONSTRAINT fk_fueltech\
            FOREIGN KEY(fueltech_id) \
            REFERENCES Dim_Fueltech(id)\
    );"
    )
    
    logger.debug("db_up: commit")
    dbc.commit()