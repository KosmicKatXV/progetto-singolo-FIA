import pandas as pd
import os.path

def importData(*args):
    if(len(args) > 1):
        fname = args[1];
    else:
        fname = 'Data.xlsx'
    if(os.path.isfile(fname)):
        return pd.read_excel(fname)
    else:
        raise Exception("No file was found or was invalid. Please check root folder and arguments.") 
    
def showNaN(data):
    print("Missing values:")
    print( data.isna().sum().where(lambda x : x!=0.00).dropna().to_string())
    
    print("samples with missing data:")
    nanSeriesRows = data.isna().sum(axis=1)
    print(nanSeriesRows.groupby(nanSeriesRows).size().where(lambda x : x!=0.00).dropna().to_string())