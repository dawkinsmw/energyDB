import pandas as pd 

def df_query(cursor,sql,id_col="id"):
    cursor.execute(sql)
    colnames = [desc[0] for desc in cursor.description]
    result = cursor.fetchall()
    result_df = pd.DataFrame(result,columns=colnames)
#     if((id_col is not None) & (id_col in colnames)):
#         result_df = result_df.set_index(id_col)
    return result_df