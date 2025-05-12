import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
#%matplotlib inline
from scipy import stats
from sklearn import linear_model
import statsmodels.formula.api as smf
import statsmodels.api as sm
import argparse
def regression (infile,clm_list_y, clm_list_x, outfile, plottitle,fig_height, fig_aspect, clm_lab_y, clm_lab_x):
    df=pd.read_csv(infile, sep="\t")
    cl = df.columns.tolist()

    clms_x = cl[int(clm_list_x)-1]
    clms_y = cl[int(clm_list_y)-1]
  
   
    #results = smf.ols('clms_y~clms_x', data=df).fit()    
    regr = linear_model.LinearRegression()
    X = df[clms_x].values.reshape(-1,1)
    y = df[clms_y].values.reshape(-1,1)
    regr.fit(X, y)
    slope, intercept, r_value, p_value, std_err = stats.mstats.linregress(df[clms_x],df[clms_y])
    a='{0:0.2f}'.format(intercept)
    b='{0:0.2f}'.format(slope)
    c='{0:0.2f}'.format(r_value)

    g = sns.lmplot(x=clms_x,y=clms_y, data=df, fit_reg=True,height= int(fig_height),aspect= float(fig_aspect),ci=None, scatter_kws={"s": int(fig_height)*8})
    g.set(xlabel=clm_lab_x, ylabel=clm_lab_y)
    props = dict(boxstyle='round', alpha=0.25,color=sns.color_palette()[0])
#textstr = '$y=1.42 + 1.27x$'
    textstr='y= {} + {}x , r={}'.format(a,b,c)
    g.ax.text(0.4, 1, textstr,transform=g.ax.transAxes, fontsize=int(fig_height)*2, bbox=props)
    plt.savefig(outfile,dpi=300,bbox_inches="tight")
    

if __name__=="__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-I", "--infile", required=True, default=None, help="Input data frame as a tab-separated (.tsv) file.")
    parser.add_argument("-Cy", "--column_list_y", required=False, default=False, help="Comma-separated list of column names to plot on the Y-axis.")
    parser.add_argument("-Cx", "--column_list_x", required=False, default=False, help="Comma-separated list of column names to plot on the X-axis.")
    parser.add_argument("-O", "--output", required=False, default='Out.png', help="Output file name for the saved figure (default: 'Out.png').")
    parser.add_argument("-T", "--title", required=False, default='Time Series plot', help="Title of the figure (default: 'Time Series plot').")
    parser.add_argument("-H", "--height", required=False, default='14', help="Figure height in inches (default: 14).")
    parser.add_argument("-A", "--aspect", required=False, default='12', help="Aspect ratio or figure width in inches (default: 12).")
    parser.add_argument("-Y", "--ylab", required=False, default='Y label', help="Label for the Y-axis (default: 'Y label').")
    parser.add_argument("-X", "--xlab", required=False, default='X label(time)', help="Label for the X-axis (default: 'X label(time)').")

    args = parser.parse_args()

    regression(args.infile, args.column_list_y, args.column_list_x, args.output, args.title, args.height, args.aspect, args.ylab, args.xlab)