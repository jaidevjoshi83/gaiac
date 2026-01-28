import pandas as pd
import os
import argparse

def align_sensor_data(file_list, date_time, sep=',', output_mode='multiple', output='aligned.tsv'):
    
    if isinstance(file_list, str):
        file_list = file_list.split(',')
        
    if len(file_list) < 2:
        print("Please provide at least two files.")
        return

    # Check if date_time is numeric (column index) or string (column name)
    use_index = False
    try:
        # User input '1' likely means 1st column (index 0)
        col_idx = int(date_time) - 1 
        if col_idx < 0:
            raise ValueError("Column index must be >= 1")
        use_index = True
        print(f"Using column index {col_idx} (from input '{date_time}')")
    except ValueError:
        # Not an integer, treat as column name
        merge_col = date_time
        print(f"Using column name '{merge_col}'")

    dfs = []
    for file in file_list:
        file = file.strip() # clean whitespace
        if not file: continue
            
        if use_index:
            # Parse dates using index
            df = pd.read_csv(file, sep=sep, parse_dates=[col_idx])

            original_col_name = df.columns[col_idx]
            merge_col = "__common_timestamp__"
            df.rename(columns={original_col_name: merge_col}, inplace=True)
        else:
            # Parse dates using name
            df = pd.read_csv(file, sep=sep, parse_dates=[date_time])
        
        dfs.append(df)

    if not dfs:
        print("No valid dataframes loaded.")
        return

    common_times = dfs[0][[merge_col]]
    for df in dfs[1:]:
        common_times = common_times.merge(df[[merge_col]], on=merge_col, how='inner')

    aligned_dfs = [
        df[df[merge_col].isin(common_times[merge_col])].reset_index(drop=True)
        for df in dfs
    ]

    
    if use_index and output_mode == 'multiple':
        for df in aligned_dfs:
            df.rename(columns={merge_col: "Date_Time"}, inplace=True)

        merge_col = "Date_Time" 

    # Output files
    if output_mode == 'single':
        # Merge all aligned dataframes
        merged_df = aligned_dfs[0]
        if use_index:
             merged_df.rename(columns={merge_col: "Date_Time"}, inplace=True)
             merge_col = "Date_Time"

        for i, df in enumerate(aligned_dfs[1:]):
             
             if use_index:
                 df.rename(columns={'__common_timestamp__': merge_col}, inplace=True)
                 
             merged_df = merged_df.merge(df, on=merge_col, how='inner')

        merged_df.to_csv(output, index=False, sep=sep)
        print("Single merged file saved.")
        
    elif output_mode == 'multiple':
         
         for i, (file, df) in enumerate(zip(file_list, aligned_dfs)):
            filename = os.path.splitext(os.path.basename(file.strip()))[0]
            output_prefix = os.path.splitext(output)[0]
            output_file = f"{output_prefix}_{filename}.tsv"
            df.to_csv(output_file, index=False, sep=sep)
         print("Aligned files saved individually.")
    else:
        print("Invalid output mode.")



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
        help='Separator used in the input files (default: tab)'
    )

    parser.add_argument(
        '-m', '--mode',
        choices=['multiple', 'single'],
        default='single',
        help="Output mode: 'multiple' for individual files, 'single' for one merged file (default: multiple)"
    )

    parser.add_argument(
        '-o', '--output',
        default='aligned.tsv',
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
