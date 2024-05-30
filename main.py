from datetime import date
import os
import json
import pandas as pd
import dataPreprocessing as dp
import sys
import argparse

lastProcess = ['uncached','fix','normalisation']
cachePath  = '.cache'

def saveFileToCache(df,fname,args,curProcess):
    #We make any cache element be useful if they share parameters and dataset
    fname = os.path.splitext(fname)[0]
    fname += args.__str__()
    #we make sure .cache exists and if not we create it
    os.makedirs(cachePath, exist_ok=True) 
    #we save the current iteration of the file
    df.to_excel(cachePath+'/'+fname+'.xlsx')
    #we read the old data
    jsonfname = cachePath+'/'+fname+'.json'
    if(os.path.isfile(jsonfname)):
        with open(jsonfname, "r") as jsonFile:
            data = json.load(jsonFile)
            #we check that it is coherent
            if(lastProcess.index(curProcess) - lastProcess.index(data['lastProc']) != 1):raise Exception('the cache is invalid')
            #if(data['time'] > date.today()): raise Exception('date is incoherent')
    else:
        data = {'lastProc':'uncached'}

    #We insert new data
    #data['time'] = date.today()
    data['lastProc'] = curProcess
    #we update the json file
    with open(jsonfname, "w") as jsonFile:
        json.dump(data,jsonFile)

def loadFileFromDataset(fname,args):
    fname = os.path.splitext(fname)[0]
    fname += args.__str__()
    jsonfname = cachePath+'/'+fname+'.json'
    if(os.path.exists(cachePath)):
        print(cachePath+'/'+fname+'.xlsx')
        if(os.path.isfile(cachePath+'/'+fname+'.xlsx') and os.path.isfile(jsonfname)):
            with open(jsonfname, "r") as jsonFile:
                data = json.load(jsonFile)
            return data['lastProc'],pd.read_excel(cachePath+'/'+fname+'.xlsx')
    return 'uncached',pd.DataFrame([])

def main():

    parser = argparse.ArgumentParser(
                    prog='Progetto FIA Singolo 2024',
                    description='Receives a dataset of patients of "neoplasia maligna" and it predicts if the next sample will be "Recidiva"',
                    epilog='by Pablo Tores Rodriguez')
    parser.add_argument('-f ',  '--filename',     type=str, default='Data.xlsx')           # positional argument
    parser.add_argument('-n',   '--neighbours',   type=int, default=2)      # option that takes a value
    parser.add_argument('-v',   '--verbose',      action='store_true')  # on/off flag
    parser.add_argument('-c',   '--cache',      action='store_true')
    args = parser.parse_args()

    #We check for a cached dataset
    if(args.cache):
        cachedProc,df = loadFileFromDataset(args.filename,args)
    else:
        cachedProc = 'uncached'

    if(lastProcess.index(cachedProc) == 0):
        print("importing dataset...")
        df = dp.importData(args.filename)
        print("Columns: %i" % len(df.columns))
        print("Rows: %i" % df.shape[0])

        #We drop the solution and index column as it would render the NaN analysis inaccurate
        sol_df = df['Recidiva/Non_Recidiva']
        index = df['ID']
        df = df.drop(columns=['Recidiva/Non_Recidiva','ID'])
    else:
        print('skipping import...')

    if(lastProcess.index(cachedProc) < 1):
        print("checking missing data...")
        dp.showNaN(df,args.verbose)
        print("fixing missing data...")
        df = dp.fixNaN(df,args.verbose,args.neighbours)
        if(args.cache):
            print('saving results to cache...')
            saveFileToCache(df,args.filename,args,lastProcess[1])
        print("checking missing data...")
        dp.showNaN(df,args.verbose)
    else:
        print('skipping NaN analysis and correction...')

    if(lastProcess.index(cachedProc) < 2):
        print("normalising dataset...")
        df = dp.normalizeDf(df)
        if(args.cache):
            print('saving results to cache...')
            saveFileToCache(df,args.filename,args,lastProcess[2])
    else:
        print('skipping normalisation...')

if __name__ == "__main__":
    main()