import pandas as pd
import dataPreprocessing as dp
import sys
import argparse

def main():

    parser = argparse.ArgumentParser(
                    prog='Progetto FIA Singolo 2024',
                    description='Receives a dataset of patients of "neoplasia maligna" and it predicts if the next sample will be "Recidiva"',
                    epilog='by Pablo Tores Rodriguez')
    parser.add_argument('-f ',  '--filename',     type=str, default='Data.xlsx')           # positional argument
    parser.add_argument('-n',   '--neighbours',   type=int, default=2)      # option that takes a value
    parser.add_argument('-v',   '--verbose',      action='store_true')  # on/off flag
    args = parser.parse_args()

    print("importing dataset...")
    df = dp.importData(args.filename)
    print("Columns: %i" % len(df.columns))
    print("Rows: %i" % df.shape[0])
    print("checking missing data...")
    dp.showNaN(df,args.verbose)
    print("fixing missing data...")
    df = dp.fixNaN(df,args.verbose,args.neighbours)
    print("checking missing data...")
    dp.showNaN(df,args.verbose)

if __name__ == "__main__":
    main()