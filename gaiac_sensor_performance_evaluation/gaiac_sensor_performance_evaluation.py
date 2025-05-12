import scipy
import os
#from scipy.stats.distributions import chi2,t
from scipy.stats import t
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
#%matplotlib inline
from scipy import stats
from sklearn import linear_model
import statsmodels.formula.api as smf
import statsmodels.api as sm
import argparse
import statsmodels.formula.api as smf
import statsmodels.api as sm
from sklearn.metrics import mean_squared_error
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-I", "--infile", required=True, default=None, help="Path to the input data file.")
parser.add_argument("-c1", "--column_1", required=True, default=None, help="Name of the first column to use.")
parser.add_argument("-c2", "--column_2", required=True, default=None, help="Name of the second column to use.")
parser.add_argument("--html_out_dir", required=False, default=os.path.join(os.getcwd(), 'report_dir'), help="Directory to save the HTML output report (default: './report_dir').")
parser.add_argument("--html_file_name", required=False, default="jai.html", help="Name of the HTML output file (default: 'jai.html').")
parser.add_argument("--workdir_path", required=False, default=os.getcwd(), help="Working directory path (default: current directory).")

args = parser.parse_args() 

if not os.path.exists(args.html_out_dir):
    os.makedirs(args.html_out_dir)

f = open(os.path.join(args.workdir_path, args.html_out_dir, args.html_file_name), 'w')

ls = range(0,6)

a1 = """
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>
    </head>

<div id="docx">
<h3> Summary Table </h3>
<div class="WordSection1">
<table table class="table table-striped">
"""

f.write(a1)

a2 = """
      </table>
  </div>
</div>

<button id="export">Export</button> Click to open table in Microsoft Word

 <script type="text/javascript">
   /* HTML to Microsoft Word Export Demo 
  * This code demonstrates how to export an html element to Microsoft Word
  * with CSS styles to set page orientation and paper size.
  * Tested with Word 2010, 2013 and FireFox, Chrome, Opera, IE10-11
  * Fails in legacy browsers (IE<10) that lack window.Blob object
  */
 window.export.onclick = function() {
 
   if (!window.Blob) {
      alert('Your legacy browser does not support this action.');
      return;
   }

   var html, link, blob, url, css;
   
   // EU A4 use: size: 841.95pt 595.35pt;
   // US Letter use: size:11.0in 8.5in;
   
   css = (
     '<style>' +
     '@page WordSection1{size: 841.95pt 595.35pt;mso-page-orientation: landscape;}' +
     'div.WordSection1 {page: WordSection1;}' +
     'table{border-collapse:collapse;}td{border:1px gray solid;width:5em;padding:2px;}'+
     '</style>'
   );
   
   html = window.docx.innerHTML;
   blob = new Blob(['\ufeff', css + html], {
     type: 'application/msword'
   });
   url = URL.createObjectURL(blob);
   link = document.createElement('A');
   link.href = url;
   // Set default file name. 
   // Word will append file extension - do not add an extension here.
   link.download = 'Document';   
   document.body.appendChild(link);
   if (navigator.msSaveOrOpenBlob ) navigator.msSaveOrOpenBlob( blob, 'Document.doc'); // IE10-11
      else link.click();  // other browsers
   document.body.removeChild(link);
 };

 </script>

 <style type="text/css">
   
   table {
  border-collapse: collapse;
}

td {
  border: 1px gray solid;
  padding: 4px;
  width: 5em;
}
 </style>

"""

###################################################33333
def RMSE(df, clms_x, clms_y):

    cl = df.columns.tolist()

    clms_x = cl[int(clms_x)-1]
    clms_y = cl[int(clms_y)-1]
    X = df[clms_x].values.reshape(-1,1)
    y = df[clms_y].values.reshape(-1,1)

    rmse = mean_squared_error(X, y)
    nrmse=(rmse/X.mean())*100
  
    return rmse, nrmse

def Reg(df, clms_x, clms_y):
    
    cl = df.columns.tolist()

    clms_x = cl[int(clms_x)-1]
    clms_y = cl[int(clms_y)-1]

    #print (clms_x, clms_y)
    #results = smf.ols('clms_y~clms_x', data=df).fit()    
    regr = linear_model.LinearRegression()
    X = df[clms_x].values.reshape(-1,1)
    y = df[clms_y].values.reshape(-1,1)
    regr.fit(X, y)
    slope, intercept, r_value, p_value, std_err = stats.mstats.linregress(df[clms_x],df[clms_y])
    a='{0:0.2f}'.format(intercept)
    b='{0:0.2f}'.format(slope)
    c='{0:0.2f}'.format(r_value)

    return a, b, c, float(c)**2

def Bias_abs(df, clm1, clm2):

    lOc = int(df.shape[0])
    cl = df.columns.tolist()

    #print (cl[int(clm1)-1], cl[int(clm2)-1])
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
       Bias_abs=round(Bias_abs*-1,2)
    elif (q1[0.25] > 0) & (q2[0.75] > 0):
       Bias_abs=round(Bias_abs,2)
    elif (q1[0.25] >0) & (q2[0.75]<0):
        Bias_abs=(u"\u00B1"+str(round(Bias_abs, 2)))
    elif (q1[0.25] <0) & (q2[0.75]>0):
        Bias_abs=(u"\u00B1"+str(round(Bias_abs, 2)))

    return Bias_abs

def R(df, clm1, clm2):
    cl = df.columns.tolist()
    results = smf.ols(str(cl[int(clm1)-1])+"~"+str(cl[int(clm2)-1]), data=df).fit()
    a = results.summary()
    #print (a)
    a = str(a).split('\n')

    l = []
    s = []

    for i in a:
        if "Intercept" in i:
            for x in i.split(' '):
                if x == '':
                    pass
                else:
                    l.append(x)

        elif (cl[int(clm2)-1] in i) and ('Dep.' not in i) :
            for x in i.split(' '):
                if x == '':
                    pass
                else:
                    s.append(x)           
    return l,s
        
#parser.add_argument("-O", "--OutFile", required=True, default=None, help="Second column")
   
df =  pd.read_csv(args.infile, sep="\t")
clm_list = df.columns.tolist()

f.write('<thead>'+'\n')
f.write('      <tr>'+'\n')
f.write('        <th>Intercept</th>'+'\n')
f.write('        <th>Slope</th>'+'\n')
f.write('        <th>r</th>'+'\n')
f.write('        <th>R Square</th>'+'\n')
f.write('        <th>RMSE</th>'+'\n')
f.write('        <th>NRMSE</th>'+'\n')
f.write('        <th>Bias</th>'+'\n')
f.write('      </tr>'+'\n')
f.write('<thead>'+'\n')

for c in args.column_1.split(','):
    _,_,r_value, r_square = Reg(df,c, args.column_2)
    b = Bias_abs(df, args.column_2, c)
    r, s= R(df, args.column_2, c)
    RMSE_v, NRMSE_v =  RMSE(df, args.column_2, c)

    f.write('      <tr>'+'\n')
    f.write('        <td>'+str(round(float(r[1]),2))+ u"\u00B1" +str(round(float(r[2]),2))+'</td>'+'\n')
    f.write('        <td>'+str(round(float(s[1]),2))+ u"\u00B1" +str(round(float(s[2]),2))+'</td>'+'\n')
    f.write('        <td>'+str(round(float(r_value),2))+'</td>'+'\n')
    f.write('        <td>'+str(round(float(r_square),2))+'</td>'+'\n')
    f.write('        <td>'+str(round(float(RMSE_v),2))+'</td>'+'\n')
    f.write('        <td>'+str(round(float(NRMSE_v),2))+'</td>'+'\n')
    f.write('        <td>'+str(b)+'</td>'+'\n')
    f.write('      <tr>'+'\n')


f.write(a2)
f.close()