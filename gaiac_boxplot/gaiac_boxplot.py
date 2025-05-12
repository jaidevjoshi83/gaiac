import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import argparse as argparse

def violinplot(infile,clm_list_y, custom_xtick_labels, outfile, plottitle,fig_height, fig_width, clm_lab_y, clm_lab_x):

    df=pd.read_csv(infile, sep="\t")
    cl = df.columns.tolist()
    clms = [cl[int(x)-1] for x in clm_list_y.split(',')]

    if custom_xtick_labels != None:
        labels  = custom_xtick_labels.split(',')
    else:
        labels  = clms
    plt.figure(figsize=(int(fig_height),int(fig_width)))
    sns.set(font_scale=0.8,style='whitegrid')
    fig=sns.boxplot(data=df[clms])
    fig.set_ylabel(clm_lab_y)
    fig.set_xlabel(clm_lab_x)
    fig.set_xticklabels(labels)
    fig.set_title(plottitle)
    plt.tight_layout
    plt.savefig(outfile,dpi=300,bbox_inches="tight")

if __name__=="__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-I", "--infile", required=True, default=None, help=".tsv")
    parser.add_argument("-C", "--column_list_y", required=False, default=False, help="Path to target tsv file")
    parser.add_argument("-L", "--custom_xtick_name", required=False, default=None, help="Path to target tsv file")
    parser.add_argument("-O", "--output", required=False, default='Out.png', help="Path to target tsv file")
    parser.add_argument("-T", "--title", required=False, default='Time Series plot', help="Path to target tsv file")
    parser.add_argument("-H", "--height", required=False, default='14', help="Path to target tsv file")
    parser.add_argument("-W", "--width", required=False, default='12', help="Path to target tsv file")
    parser.add_argument("-Y", "--ylab", required=False, default='Y label', help="Path to target tsv file")
    parser.add_argument("-X", "--xlab", required=False, default='X label(time)', help="Path to target tsv file")
    args = parser.parse_args()

    violinplot(args.infile, args.column_list_y, args.custom_xtick_name, args.output, args.title, args.width, args.height, args.ylab, args.xlab)
