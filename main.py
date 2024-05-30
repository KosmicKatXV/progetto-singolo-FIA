import pandas as pd
import dataPreprocessing as dp

def main():
    df = dp.importData()
    print(df.columns.to_list())
    print("Columns: %i" % len(df.columns))
    print("Rows: %i" % df.shape[0])
    #dp.showNaN(df)

if __name__ == "__main__":
    main()