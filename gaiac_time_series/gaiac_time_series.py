import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import argparse
#%matplotlib inline

def timeseries(infile,clm_list_y, custom_legend_label, outfile, plottitle,fig_height, fig_width, clm_lab_y, clm_lab_x):

    df=pd.read_csv(infile, sep="\t")

    cl = df.columns.tolist()

    clms = [cl[int(x)-1] for x in clm_list_y.split(',')]

    if custom_legend_label != None:
        labels  = custom_legend_label.split(',')
    else:
        labels  = clms

    g=(df[clms].plot(figsize=(int(fig_height),int(fig_width))))
    g.set(ylabel=clm_lab_y, xlabel=clm_lab_x)
    plt.legend(labels, ncol=2, loc='upper right',prop={'size': 6})
    plt.savefig(outfile,dpi=300,bbox_inches="tight")


if __name__=="__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-I", "--infile", required=True, default=None, help="Input data file in TSV format.")
    parser.add_argument("-C", "--column_list_y", required=False, default=False, help="Comma-separated list of column names for Y-axis data.")
    parser.add_argument("-L", "--custom_legend_name", required=False, default=None, help="Custom legend names as a comma-separated list (optional).")
    parser.add_argument("-O", "--output", required=False, default='Out.png', help="Filename for the output plot image (default: 'Out.png').")
    parser.add_argument("-T", "--title", required=False, default='Time Series plot', help="Title of the plot (default: 'Time Series plot').")
    parser.add_argument("-H", "--height", required=False, default='14', help="Height of the figure in inches (default: 14).")
    parser.add_argument("-W", "--width", required=False, default='12', help="Width of the figure in inches (default: 12).")
    parser.add_argument("-Y", "--ylab", required=False, default='Y label', help="Label for the Y-axis (default: 'Y label').")
    parser.add_argument("-X", "--xlab", required=False, default='X label(time)', help="Label for the X-axis (default: 'X label(time)').")

    args = parser.parse_args()

    timeseries(args.infile, args.column_list_y, args.custom_legend_name, args.output, args.title, args.width, args.height, args.ylab, args.xlab)


#plt.show()