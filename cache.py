import json
import os
import hashlib
import pandas as pd


lastProcess = ['uncached','fix','normalisation','feature_selection']
cachePath  = '.cache'

def saveFileToCache(df,args,curProcess,dfName):
    print('saving results to cache...')
    #We make any cache element be useful if they share parameters and dataset
    fname = dfName
    fname += hashlib.sha256((args.__str__()+os.path.splitext(args.filename)[0]).encode('ascii')).hexdigest()
    #we make sure .cache exists and if not we create it
    os.makedirs(cachePath, exist_ok=True) 
    #we save the current iteration of the file
    df.to_excel(cachePath+'/'+fname+'.xlsx',index=False)
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

def loadFileFromDataset(dfName,args):
    fname = dfName
    fname += hashlib.sha256((args.__str__()+os.path.splitext(args.filename)[0]).encode('ascii')).hexdigest()
    jsonfname = cachePath+'/'+fname+'.json'
    if(os.path.exists(cachePath)):
        if(os.path.isfile(cachePath+'/'+fname+'.xlsx') and os.path.isfile(jsonfname)):
            with open(jsonfname, "r") as jsonFile:
                data = json.load(jsonFile)
            return data['lastProc'],pd.read_excel(cachePath+'/'+fname+'.xlsx')
    return 'uncached',pd.DataFrame([])

def removeFileFromDataset(dfName,args):
    fname = dfName
    fname += hashlib.sha256((args.__str__()+os.path.splitext(args.filename)[0]).encode('ascii')).hexdigest()
    jsonfname = cachePath+'/'+fname+'.json'
    if(os.path.exists(cachePath)):
        if(os.path.isfile(cachePath+'/'+fname+'.xlsx') and os.path.isfile(jsonfname)):
            os.remove(jsonfname)
            os.remove(cachePath+'/'+fname+'.xlsx')
def getProcessList():
    return lastProcess