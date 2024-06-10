from datetime import date
import hashlib
import json
import os
from sklearn.metrics import classification_report

target_names = ['Recidiva', 'Non recidiva']

def report(y_true,y_pred,v):
    #We divide cm in several variables for clarity
    output = classification_report(y_true, y_pred, target_names=target_names,output_dict=True)
    if(v): print(classification_report(y_true, y_pred, target_names=target_names))
    return output

def save(report,args):
    #We make any cache element be useful if they share parameters and dataset
    fname = os.path.splitext(args.filename)[0]
    fname += hashlib.sha256(args.__str__().encode('ascii')).hexdigest()
    #we make sure .cache exists and if not we create it
    os.makedirs(args.output, exist_ok=True) 
    #we save the current iteration of the file
    #we read the old data
    jsonfname = args.output+'/'+fname+'.json'
    report['time'] = date.today().__str__()
    report.update(args.__dict__)
    #we update the json file
    with open(jsonfname, "w") as jsonFile:
        json.dump(report,jsonFile)