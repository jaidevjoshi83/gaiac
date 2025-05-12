import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import argparse
#%matplotlib inline

def ScatterPlot(InFile, PlotingOptionforx, PlotingOptionfory, xclm1, xclm2, yclm1, yclm2,outfile, plottitle,fig_height, fig_width, clm_lab_y, clm_lab_x):

    df = pd.read_csv(InFile, sep="\t")
    clm_list = df.columns.tolist()

    if PlotingOptionforx == 'simple':
        dfx = df[clm_list[int(xclm1)-1]]

    elif PlotingOptionforx == 'advance':
        dfx = pd.DataFrame()
        dfx['ratiox'] = df[clm_list[int(xclm1)-1]]/df[clm_list[int(xclm2)-1]]

    if PlotingOptionfory == 'simple':
        dfy = df[clm_list[int(yclm1)-1]]

    elif PlotingOptionfory == 'advance':
        dfy = pd.DataFrame()
        dfy['ratioy'] = df[clm_list[int(yclm1)-1]]/df[clm_list[int(yclm2)-1]]

    df = pd.concat([dfx, dfy], axis=1)

    print (df)

    df.columns.tolist()[0]

    #plt.figure(figsize=(8,6))
    plt.figure(figsize=(int(fig_width),int(fig_height)))
    g = sns.lmplot(x=df.columns.tolist()[0], y=df.columns.tolist()[1],data=df,lowess=True,aspect=1.1,ci=None, scatter_kws={"s": 100})
    g.set(ylabel=clm_lab_y, xlabel=clm_lab_x)
    #plt.show()
    plt.savefig(outfile,dpi=300,bbox_inches="tight")

if __name__=="__main__":

    parser = argparse.ArgumentParser(description="Generate a customized plot from a .tsv file with specified plotting options.")

    parser.add_argument(
        "-I", "--infile", 
        required=True, 
        help="Input .tsv file containing the data to be plotted."
    )

    parser.add_argument(
        "-px", "--plotting_option_for_x", 
        required=True,  
        help="Plotting option for the X-axis (e.g., line, scatter)."
    )

    parser.add_argument(
        "-py", "--plotting_option_for_y", 
        required=True,  
        help="Plotting option for the Y-axis (e.g., line, scatter)."
    )

    parser.add_argument(
        "-c1", "--x_column_1", 
        required=True, 
        help="Column name in the .tsv file for the primary X-axis data."
    )

    parser.add_argument(
        "-c2", "--x_column_2", 
        required=False, 
        default=None, 
        help="Optional second column name for the X-axis."
    )

    parser.add_argument(
        "-c3", "--y_column_1", 
        required=True, 
        help="Column name in the .tsv file for the primary Y-axis data."
    )

    parser.add_argument(
        "-c4", "--y_column_2", 
        required=False, 
        default=None, 
        help="Optional second column name for the Y-axis."
    )

    parser.add_argument(
        "-O", "--output", 
        required=False, 
        default='Out.png', 
        help="Output file name for the generated plot image (default: Out.png)."
    )

    parser.add_argument(
        "-T", "--title", 
        required=False, 
        default='Time Series plot', 
        help="Title of the plot (default: 'Time Series plot')."
    )

    parser.add_argument(
        "-H", "--height", 
        required=False, 
        default='14', 
        help="Height of the plot figure in inches (default: 14)."
    )

    parser.add_argument(
        "-W", "--width", 
        required=False, 
        default='12', 
        help="Width of the plot figure in inches (default: 12)."
    )

    parser.add_argument(
        "-Y", "--ylab", 
        required=False, 
        default='Y label', 
        help="Label for the Y-axis (default: 'Y label')."
    )

    parser.add_argument(
        "-X", "--xlab", 
        required=False, 
        default='X label (time)', 
        help="Label for the X-axis (default: 'X label (time)')."
    )

    args = parser.parse_args()

    ScatterPlot(args.infile, args.plotting_option_for_x, args.plotting_option_for_y, args.x_column_1, args.x_column_2, args.y_column_1, args.y_column_2, args.output, args.title, args.height, args.width, args.ylab, args.xlab)










