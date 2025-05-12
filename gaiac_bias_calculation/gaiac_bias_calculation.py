import scipy
#from scipy.stats.distributions import chi2,t
from scipy.stats import t
from scipy import stats
import pandas as pd
import numpy as np
import argparse

def Bias_abs(infile, clm1, clm2, Out):

    df = pd.read_csv(infile, sep="\t")
    lOc = int(df.shape[0])
    cl = df.columns.tolist()
#making a column of absolute di as per us epa
    df['PM10_OPC_DIFF']=abs(((df[cl[int(clm1)-1]])-(df[cl[int(clm2)-1]]))/(df[cl[int(clm2)-1]]))*100
#square of di
    df['PM10_OPC_DIFFs']=(df['PM10_OPC_DIFF'])*(df['PM10_OPC_DIFF'])
#summation of the columns
    d10=df.PM10_OPC_DIFF.sum()
    d10_2=df.PM10_OPC_DIFFs.sum()
#AB and AS calculations
    AB= d10/lOc
    AS=(np.sqrt((lOc*(d10_2)-(d10)**2)/(2*lOc*(lOc-1))))
    
#T distribution calculation
    T=stats.t.ppf(1-0.05, lOc)
#Absolute bias calculation    
    Bias_abs = abs(AB + T*AS/(np.sqrt(lOc)))
    
#di column with sign 
    df['Di']=(((df[cl[int(clm1)-1]])-(df[cl[int(clm2)-1]]))/(df[cl[int(clm2)-1]]))*100
#quantiles of di without sign
    q1=df['Di'].quantile([0.25])
    q2=df['Di'].quantile([0.75])
#assigning sign to absolute bias based on q1 and q2 values

    if (q1[0.25] < 0) & (q2[0.75] < 0):
       Bias_abs=Bias_abs*-1
    elif (q1[0.25] > 0) & (q2[0.75] > 0):
       Bias_abs=Bias_abs
    elif (q1[0.25] >0) & (q2[0.75]<0):
        Bias_abs=(u"\u00B1"+str(Bias_abs))
    elif (q1[0.25] <0) & (q2[0.75]>0):
        Bias_abs=(u"\u00B1"+str(Bias_abs))

#output file
    df1 = pd.DataFrame([Bias_abs], columns=['Percent Bias'])
    df1.round(4).to_csv(Out, sep="\t")


if __name__=="__main__":
    
    parser = argparse.ArgumentParser()

    parser.add_argument("-I", "--infile", required=True, default=None, help="Input file")
    parser.add_argument("-c1", "--column_1", required=True, default=None, help="First column")
    parser.add_argument("-c2", "--column_2", required=True, default=None, help="Second column")
    parser.add_argument("-o", "--output", required=True, default=None, help="OutFile")                           
    args = parser.parse_args()

    Bias_abs(args.infile, args.column_1, args.column_2, args.output)
