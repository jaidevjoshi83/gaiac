import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import argparse
from windrose import WindroseAxes

def wind_rose (infile, clm_list_dir, clm_list_ws, outfile):
    df=pd.read_csv(infile, sep="\t")
    cl = df.columns.tolist()

    clms_dir = cl[int(clm_list_dir)-1]
    clms_ws = cl[int(clm_list_ws)-1]

    ax = WindroseAxes.from_ax()
    ax.bar(df[clms_dir], df[clms_ws], normed=True, opening=0.8, edgecolor='white')
    ax.set_legend(bbox_to_anchor=(1.05, 0.5))
    ax.set_xticklabels(['W', 'NW',  'N', 'NE', 'E', 'SE','S', 'SW'])

    plt.savefig(outfile, dpi=300,bbox_inches="tight")
   

if __name__=="__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-I", "--infile", required=True, default=None, help=".tsv")
    parser.add_argument("-d", "--column_list_dir", required=False, default=False, help="Path to target tsv file")
    parser.add_argument("-w", "--column_list_ws", required=False, default=False, help="Path to target tsv file")
    parser.add_argument("-O", "--output", required=False, default='Out.png', help="Path to target tsv file")
    
    args = parser.parse_args()

    wind_rose(args.infile, args.column_list_dir, args.column_list_ws, args.output)