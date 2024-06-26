import pandas as pd
import numpy as np
import os.path
from sklearn.impute import KNNImputer
from sklearn import preprocessing
import statsmodels.api as smf

def importData(fname):
    if(os.path.isfile(fname)):
        return pd.read_excel(fname)
    else:
        raise Exception("No file was found or was invalid. Please check root folder and arguments.") 
    
def showNaN(data):
    print("Columns with missing values: %i" % data.isna().any(axis=0).sum())
    print( data.isna().sum().where(lambda x : x!=0.00).dropna().to_string())
    print("Rows with missing data: %i" % data.isna().any(axis=1).sum())
    nanSeriesRows = data.isna().sum(axis=1)
    print(nanSeriesRows.groupby(nanSeriesRows).size().where(lambda x : x!=0.00).dropna().to_string())

def fixNaN(data,verbose,n):
    nan_columns = data.isna().columns
    nan_df= data.isna()
    nan_array = nan_df.to_numpy()
    if(verbose): print("Columns with missing data:")
    if(verbose): print(nan_df.dtypes.to_string()) #We can see that missin values are either float or integers so we apply a fitting algorithm
    imputer = KNNImputer(n_neighbors=2, weights="uniform")
    imputer.set_output(transform='pandas')
    nan_df = imputer.fit_transform(nan_array)
    nan_df.columns = nan_columns
    return data.fillna(nan_df)

def normalizeDf(data):
    d = preprocessing.normalize(data, axis=0)
    return pd.DataFrame(d, columns=data.columns)

def getLabeled(data,solData):
    data['Recidiva/Non_Recidiva'] = solData['Recidiva/Non_Recidiva']
    return data.dropna(axis=0).drop(columns=['Recidiva/Non_Recidiva']),solData.dropna(axis=0)

def featureSelection(x,y,p):
    return x,y