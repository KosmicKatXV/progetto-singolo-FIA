from datetime import date
import os
import json
import numpy as np
import pandas as pd
from cache import getProcessList, loadFileFromDataset, saveFileToCache
import dataPreprocessing as dp
import classification as cl
import evaluation as ev
import sys
import argparse

def main():

    parser = argparse.ArgumentParser(
                    prog='Progetto FIA Singolo 2024',
                    description='Receives a dataset of patients of "neoplasia maligna" and it predicts if the next sample will be "Recidiva"',
                    epilog='by Pablo Tores Rodriguez')
    parser.add_argument('-f ',  '--filename',      type=str,    default='Data.xlsx')           # positional argument
    parser.add_argument('-n',   '--neighbours',    type=int,    default=2)      # option that takes a value
    parser.add_argument('-ts',  '--testsize',      type=float,  default=0.2)
    parser.add_argument('-m',   '--model',         type=str,    default='knn')
    parser.add_argument('-r',   '--regularisation',type=float,  default=1.0)
    parser.add_argument('-p',   '--penalty',       type=str,    default=None)
    parser.add_argument('-o',   '--output',        type=str,    default='results/')
    parser.add_argument('-v',   '--verbose',       action='store_true')  # on/off flag
    parser.add_argument('-c',   '--cache',         action='store_true')
    args = parser.parse_args()

    lastProcess = getProcessList()

    #We check for a cached dataset
    if(args.cache):
        cachedProc,df = loadFileFromDataset("df",args)
        _,df_sol = loadFileFromDataset("df_sol",args)
    else:
        cachedProc = 'uncached'

    if(lastProcess.index(cachedProc) == 0):
        if(args.verbose): print("importing dataset...")
        df = dp.importData(args.filename)
        if(args.verbose):
            print("Columns: %i" % len(df.columns))
            print("Rows: %i" % df.shape[0])

        #We drop the solution and index column as it would render the NaN analysis inaccurate
        sol_df = df[['Recidiva/Non_Recidiva']]
        df = df.drop(columns=['Recidiva/Non_Recidiva','ID'])
    else:
        if(args.verbose): print('skipping import...')

    if(lastProcess.index(cachedProc) < 1):
        if(args.verbose):
            print("checking missing data...")
            dp.showNaN(df)
            print("fixing missing data...")
        df = dp.fixNaN(df,args.verbose,args.neighbours)
        if(args.cache):
            saveFileToCache(df,args,lastProcess[1],"df")
            saveFileToCache(df_sol,args,lastProcess[1],"df_sol")
        if(args.verbose):
            print("checking missing data...")
            dp.showNaN(df)
    else:
        if(args.verbose): print('skipping NaN analysis and correction...')

    if(lastProcess.index(cachedProc) < 2):
        if(args.verbose): print("normalising dataset...")
        df = dp.normalizeDf(df)
        if(args.cache):
            saveFileToCache(df,args,lastProcess[2],"df")
    else:
        if(args.verbose): print('skipping normalisation...')
    
    #We proceed to create a new dataframe with only label data to correct assess which features are more relevant
    if(lastProcess.index(cachedProc) < 3):
        if(args.verbose): print("feature selection in progress...")
        x,y = dp.featureSelection(df,sol_df,0.05)
        if(args.cache):
            saveFileToCache(df,args,lastProcess[3],"df")
    else:
        if(args.verbose): print('skipping feature selection...')
    
    if(args.verbose): print("data classification in progress...")
    y_test,y_pred = cl.classify(df,sol_df,args)

    if(args.verbose): print("data evaluation in progress...")
    rep = ev.report(y_test,y_pred,args.verbose)

    if(args.verbose): print('saving results to %s...' % args.output)
    ev.save(rep,args)

if __name__ == "__main__":
    main()