import pandas as pd
import os
import argparse

def align_sensor_data(file_list, date_time, sep=',', output_mode='multiple', output='aligned.tsv'):
    
    file_list =  file_list.split(',')
    if len(file_list) < 2:
        print("Please provide at least two files.")
        return

    # Read all files into a list of dataframes
    dfs = [pd.read_csv(file, sep=sep, parse_dates=[date_time]) for file in file_list]

    # Get common timestamps by successive inner merges
    common_times = dfs[0][[date_time]]
    for df in dfs[1:]:
        common_times = common_times.merge(df[[date_time]], on=date_time, how='inner')

    # Now filter each dataframe to contain only common timestamps
    aligned_dfs = [
        df[df[date_time].isin(common_times[date_time])].reset_index(drop=True)
        for df in dfs
    ]

    # Output files
    if output_mode == 'multiple':
        for i, (file, df) in enumerate(zip(file_list, aligned_dfs)):
            filename = os.path.splitext(os.path.basename(file))[0]
            output_file = f"{output_prefix}_{filename}.csv"
            df.to_csv(output_file, index=False, sep=sep)
        print("Aligned files saved individually.")
    elif output_mode == 'single':
        # Merge all aligned dataframes on date_time
        merged_df = aligned_dfs[0]
        for df in aligned_dfs[1:]:
            merged_df = merged_df.merge(df, on=date_time, how='inner')

       
        merged_df.to_csv(output, index=False, sep=sep)
        print("Single merged file saved.")
    else:
        print("Invalid output mode. Use 'multiple' or 'single'.")


def main():
    parser = argparse.ArgumentParser(description="Align sensor data files on common timestamps.")

    parser.add_argument(
        '-f', '--files',
        required=True,
        help='List of input file paths (at least two)'
    )

    parser.add_argument(
        '-s', '--sep',
        default='\t',
        help='Separator used in the input files (default: ,)'
    )

    parser.add_argument(
        '-m', '--mode',
        choices=['multiple', 'single'],
        default='single',
        help="Output mode: 'multiple' for individual files, 'single' for one merged file (default: multiple)"
    )

    parser.add_argument(
        '-o', '--output',
        default='aligned',
        help="Output filename"
    )

    parser.add_argument(
        '-t', '--date_time_column',
        default='date_time',
        help="Provide the name of the date and time column."
    )

    args = parser.parse_args()

    align_sensor_data(
        file_list=args.files,
        date_time=args.date_time_column,
        sep=args.sep,
        output_mode=args.mode,
        output=args.output
    )

if __name__ == '__main__':
    main()
