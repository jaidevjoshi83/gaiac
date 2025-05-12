import pandas as pd
import argparse

#This tool would average your time series data based on the time intervals based on the time and date column 
#python avg_timeseries.py -I data.tsv -C 1 -T 5 -O averaged_output.tsv


def main():
    parser = argparse.ArgumentParser(description="Average time series data over specified intervals.")
    parser.add_argument("-I", "--infile", required=True, help="Input data file (TSV format)")
    parser.add_argument("-C", "--dt_column", required=True, help="Column number (1-based) for the DateTime column")
    parser.add_argument("-T", "--time_interval", required=True, help="Time interval in minutes, e.g., '5' or '30'")
    parser.add_argument("-O", "--out_file", default='OutFile.tsv', help="Output file name (TSV format)")
    parser.add_argument("-S", "--sep", default='\t', help="deliminator")

    args = parser.parse_args()

    # Load data
    data = pd.read_csv(args.infile, sep=args.sep)

    # Extract the correct datetime column name
    col_index = int(args.dt_column) - 1  # Convert 1-based index to 0-based
    datetime_col = data.columns[col_index]

    # Set datetime index
    data[datetime_col] = pd.to_datetime(data[datetime_col], errors='coerce')
    data.set_index(datetime_col, inplace=True)

    # Group by time intervals and compute mean for numeric columns
    df_avg = data.resample(f'{args.time_interval}Min').mean(numeric_only=True)

    # Round to 3 decimals and save to output file
    df_avg.round(3).to_csv(args.out_file, sep='\t')

    print(f"Averaged data saved to {args.out_file}")

if __name__ == "__main__":
    main()
