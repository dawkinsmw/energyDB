import pandas as pd
from src.query.utils import df_query

def insert_carbon_factors(cursor,logger):
    logger.debug('insert_carbon_factors')
    co2_parameters = pd.read_csv("../../../data/co2_parameters.csv",index_col=1)
    co2_parameters.index = co2_parameters.index.str.lower()
    co2_parameters = co2_parameters.drop(columns=["Uid"])

    Fact_CarbonFactor = df_query(cursor,
    "select \
        dim_network.id as network_id,\
        dim_region.id as region_id,\
        dim_fueltech.id as fueltech_id,\
        dim_region.short_name,\
        dim_fueltech.long_name \
    from dim_network, dim_region, dim_fueltech"
    )
    Fact_CarbonFactor["carbon_factor"] = 0
    for i in range(Fact_CarbonFactor.shape[0]):
        region, fueltech = Fact_CarbonFactor.iloc[i][["short_name","long_name"]]
        Fact_CarbonFactor.loc[i,"carbon_factor"] =  co2_parameters.loc[fueltech,region]
    Fact_CarbonFactor = Fact_CarbonFactor[["network_id","region_id","fueltech_id","carbon_factor"]]

    data = Fact_CarbonFactor[Fact_CarbonFactor["carbon_factor"].notnull()]
    for i in range(data.shape[0]):
        network_id,region_id,fueltech_id,carbon_factor = data.iloc[i][["network_id","region_id","fueltech_id","carbon_factor"]]
        cursor.execute(
        f"INSERT INTO Fact_CarbonFactor(network_id,region_id,fueltech_id,carbon_factor) VALUES ({network_id},{region_id},{fueltech_id},{carbon_factor})"
                    )