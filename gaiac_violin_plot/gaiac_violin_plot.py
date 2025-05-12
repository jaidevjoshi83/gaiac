import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
#%matplotlib inline
import argparse as argparse
def violinplot(infile, clm_list_y, custom_xtick_labels, outfile, plottitle, fig_height, fig_width, clm_lab_y, clm_lab_x):

    df=pd.read_csv(infile, sep="\t")

    cl = df.columns.tolist()

    clms = [cl[int(x)-1] for x in clm_list_y.split(',')]

    if custom_xtick_labels != None:
        labels  = custom_xtick_labels.split(',')
        #print(labels)
    else:
        labels  = clms
    plt.figure(figsize=(int(fig_height),int(fig_width)))
    sns.set(font_scale=0.8,style='whitegrid')
    fig=sns.violinplot(data=df[clms])
    fig.set_ylabel(clm_lab_y)
    fig.set_xlabel(clm_lab_x)
    fig.set_xticklabels(labels)
    fig.set_title(plottitle)
    plt.tight_layout
    plt.savefig(outfile,dpi=300,bbox_inches="tight")


if __name__=="__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-I", "--infile", required=True, default=None, help="Input data file in TSV (tab-separated) format.")
    parser.add_argument("-C", "--column_list_y", required=False, default=False, help="Comma-separated list of column names to plot on the Y-axis.")
    parser.add_argument("-L", "--custom_xtick_name", required=False, default=None, help="Comma-separated list of custom legend names for the plot legend.")
    parser.add_argument("-O", "--output", required=False, default='Out.png', help="Filename for the output plot image (e.g. 'plot.png').")
    parser.add_argument("-T", "--title", required=False, default='Time Series plot', help="Title of the time series plot.")
    parser.add_argument("-H", "--height", required=False, default='14', help="Height of the figure in inches (default: 14).")
    parser.add_argument("-W", "--width", required=False, default='12', help="Width of the figure in inches (default: 12).")
    parser.add_argument("-Y", "--ylab", required=False, default='Y label', help="Label for the Y-axis (default: 'Y label').")
    parser.add_argument("-X", "--xlab", required=False, default='X label(time)', help="Label for the X-axis (default: 'X label(time)').")

    args = parser.parse_args()

    violinplot(args.infile, args.column_list_y, args.custom_xtick_name, args.output, args.title, args.width, args.height, args.ylab, args.xlab)
