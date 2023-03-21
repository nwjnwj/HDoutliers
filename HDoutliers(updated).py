import pandas as pd
import numpy as np
import math
import prince
from pandas.api.types import is_numeric_dtype

def dataTrans(data):
    ## data:pd.DataFrame
    if data.isnull().any().sum()  > 0 :
        raise ValueError("missing values not allowed")

    cte = {}
    for col in data.columns: 
        cte[col] = (len(data[col].drop_duplicates())==1)
    if all(cte.values()):
        print("[Warning] all columns have a constant values")
        return None
    elif any(cte.values()):
        print("some columns have a constant values")

    ## del
    for col in data.columns:
        if cte[col]:del data[col]

    CAT = {}
    for col in data.columns: 
        CAT[col] = is_numeric_dtype(data[col])

    if any(CAT.values()):
        mca = prince.MCA(n_components=1,)
        for k,v in CAT.items():
            if not v:
                k_numpy = data[k].to_numpy().reshape(-1, 1)
                data[k] = mca.fit(k_numpy).transform(k_numpy)

    def unitize(col):
        col_min, col_max = col.min(), col.max()
        if col_min == col_max: 
            return 0
        else:
            return col.apply(lambda x: (x-col_min)/(col_max-col_min))
    for col in data.columns:
        data[col] = unitize(data[col])

    return data


def getHDmembers(data, maxrows = 10000, radius = None):
    ## data:pd.DataFrame
    n = len(data)
    p = len(data.columns)
    if radius is None:
        radius = 0.1/(math.log(n)**(1/p))

    data = data.reset_index(drop=True)
    if n <= maxrows:
        ## 
        m = len(data.drop_duplicates(keep='first'))
        members = list(data.index)
    else:
        members = [0] * n
        exemplars = 1
        members[0] = 1
        for i in range(1,n):
            ##get.knn
            pass



    return members