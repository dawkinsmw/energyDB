## Codes
from data.emission_factors import emissions_factors

## Insert batch
def insert_emission_factors(cursor,logger):

    ## FACT_X_CAP
    for ft in emissions_factors.keys():
        try:
            cursor.execute(
                f"INSERT INTO Dim_Fueltech(emissions_factor) \
                VALUES ('{emissions_factors[ft]}') \
                WHERE long_name = {ft}"
            )
        except Exception as e:
            logger.error(f"Failed to insert {ft} emissions factor")
            logger.error(e)

