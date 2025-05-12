import scipy
import argparse
from scipy.stats.distributions import chi2
import pandas as pd
import numpy as np

def Precision(infile, clm1, clm2, Out):

	df = pd.read_csv(infile, sep="\t")
	lOc = int(df.shape[0])

	cl = df.columns.tolist()

	df['PM10_OPC_DIFF']=(((df[cl[int(clm1)-1]])-(df[cl[int(clm2)-1]]))/(((df[cl[int(clm1)-1]])+(df[cl[int(clm2)-1]]))/2)*100)
	df['PM10_OPC_DIFFs']=(df['PM10_OPC_DIFF'])*(df['PM10_OPC_DIFF'])
	d10=df.PM10_OPC_DIFF.sum()
	d10_2=df.PM10_OPC_DIFFs.sum()
	CV_10= (np.sqrt((lOc*(d10_2)-(d10)**2)/(2*lOc*(lOc-1))))*(np.sqrt((lOc-1)/(chi2.ppf(0.1, df=lOc))))
	df1 = pd.DataFrame([CV_10], columns=['Percent Precision'])
	df1.round(4).to_csv(Out,sep='\t')

if __name__=="__main__":
    
    parser = argparse.ArgumentParser()

    parser.add_argument("-I", "--infile", required=True, default=None, help="Input file")
    parser.add_argument("-c1", "--column_1", required=True, default=None, help="First column")
    parser.add_argument("-c2", "--column_2", required=True, default=None, help="Second column")
    parser.add_argument("-o", "--out", required=True, default=None, help="OutFile")                           
    args = parser.parse_args()

    Precision(args.infile, args.column_1, args.column_2, args.out)
