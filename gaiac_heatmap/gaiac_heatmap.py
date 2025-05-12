import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import argparse
#%matplotlib inline

def HeatMap(infile, clm_list, custom_column_labels, outfile, plottitile, fig_height, fig_width):

    df=pd.read_csv(infile, sep="\t")
    cl = df.columns.tolist()
    clms = [ cl[int(x)-1] for x in clm_list.split(',')]

    if custom_column_labels != None:
        labels  = custom_column_labels.split(',')
    else:
        labels  = clms

    sns.set(font_scale=0.6,style='whitegrid')
    plt.figure(figsize=(int(fig_height), int(fig_width)))
    ax = sns.heatmap(df[clms].corr(),annot=True,xticklabels=labels,yticklabels=labels,fmt='.2g')
    bottom, top = ax.get_ylim()
    ax.set_ylim(bottom + 0.5, top - 0.5)
    plt.savefig(outfile,dpi=300,bbox_inches="tight")

if __name__=="__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-I", "--infile", required=True, default=None, help=".tsv")
    parser.add_argument("-C", "--column_list", required=False, default=False, help="Path to target tsv file")
    parser.add_argument("-L", "--custom_column_name", required=False, default=None, help="Path to target tsv file")
    parser.add_argument("-O", "--output", required=False, default='Out.png', help="Path to target tsv file")
    parser.add_argument("-T", "--title", required=False, default='Correlation plot', help="Path to target tsv file")
    parser.add_argument("-H", "--height", required=False, default='14', help="Path to target tsv file")
    parser.add_argument("-W", "--width", required=False, default='12', help="Path to target tsv file")

    args = parser.parse_args()

    HeatMap(args.infile, args.column_list, args.custom_column_name, args.output, args.title, args.width, args.height)