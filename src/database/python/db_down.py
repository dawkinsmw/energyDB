
def db_down(dbc):
    cur = dbc.cursor()
    cur.execute(
        f"DROP TABLE IF EXISTS Fact_CarbonFactor;\
        DROP TABLE IF EXISTS Fact_X_Cap;\
        DROP TABLE IF EXISTS Fact_Price;\
        DROP TABLE IF EXISTS Fact_Power;\
        DROP TABLE IF EXISTS Dim_Batch;\
        DROP TABLE IF EXISTS Dim_Region;\
        DROP TABLE IF EXISTS Dim_Network;\
        DROP TABLE IF EXISTS Dim_Fueltech;"
    )
    dbc.commit()