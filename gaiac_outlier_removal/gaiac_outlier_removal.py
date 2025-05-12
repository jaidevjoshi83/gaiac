import numpy as np
import pandas as pd

# python 'outlier_removal.py' -I '' -M 'replace' -QU '75' -QL '25' -MU '1.5'


def AddMedian(input_data, column_list, out_file, method='drop', Q_UP=75, Q_DOWN=25, Multiplier=1.5, sep='\t'):
    df = pd.read_csv(input_data, sep=sep)
    cl = df.columns.tolist()
    
    clms = [cl[int(x)-1] for x in column_list.split(',')]

    Q_UP = float(Q_UP)
    Q_DOWN = float(Q_DOWN)
    Multiplier = float(Multiplier)

    if method == 'replace':
        for col in clms:
            q75, q25 = np.percentile(df[col], [Q_UP, Q_DOWN])
            intr_qr = q75 - q25
            upper_bound = q75 + (Multiplier * intr_qr)
            lower_bound = q25 - (Multiplier * intr_qr)

            median_val = np.median(df[col])
            df.loc[df[col] < lower_bound, col] = median_val
            df.loc[df[col] > upper_bound, col] = median_val

    elif method == "drop":
        # compute bounds for each column
        for col in clms:
            Q1 = np.percentile(df[col], 25, interpolation='midpoint')
            Q3 = np.percentile(df[col], 75, interpolation='midpoint')
            IQR = Q3 - Q1

            upper_bound = Q3 + (Multiplier * IQR)
            lower_bound = Q1 - (Multiplier * IQR)

            # drop rows where col value is an outlier
            df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]

    else:
        raise ValueError("Invalid method. Choose 'drop' or 'replace'.")

    df.to_csv(out_file, sep="\t", index=None)       


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Outlier removal or replacement tool")

    parser.add_argument("-I", "--infile", required=True, help="Path to input TSV file")
    parser.add_argument("-C", "--column_list", required=True, help="Comma-separated list of 1-based column numbers to process")
    parser.add_argument("-O", "--outfile", required=True, help="Output TSV file path")
    parser.add_argument("-M", "--method", required=True, choices=["drop", "replace"], help="Select whether to 'drop' outliers or 'replace' with median")
    parser.add_argument("-QU", "--upper_quartile", default=75, help="Upper quartile value (default 75)")
    parser.add_argument("-QL", "--lower_quartile", default=25, help="Lower quartile value (default 25)")
    parser.add_argument("-MU", "--multiplier_constant", default=1.5, help="IQR multiplier constant (default 1.5)")
    parser.add_argument("-S", "--sep", default='\t', help="deliminator")

    args = parser.parse_args()

    AddMedian(args.infile, args.column_list, args.outfile, args.method, args.upper_quartile, args.lower_quartile, args.multiplier_constant, args.sep)
