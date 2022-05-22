import numpy as np
import pandas as pd
import argparse
import os
import time
import datetime

class ExcelProcessing(object):
    def __init__(self, excel_file):
        self.df = excel_file

    def drop_columns(self):
        '''
        Drop columns that aren't useful
        '''
        tmp_df = self.df.drop(columns=["Weight Tracker","Start Date"], axis = 1)
        tmp_df = tmp_df[3:] #Formatting of the excel sheet is bad. Start from col3
        return tmp_df

    def rename_headers(self, df):
        '''
        Rename in place
        df_new_headers = drop_columns.rename_headers(df)
        '''
        tmp_df = df.copy()
        tmp_df.columns = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday','Average']
        tmp_df = tmp_df.reset_index().drop('index', axis = 1)
        return tmp_df

class WeightConverter():
    '''
    Should take in df from ExcelProcessing()
    '''
    def __init__(self, df):
        self.df = df #ExcelProcessing().rename_headers()

    def weights_only(self):
        '''
        Create df with rows as days, columns as weeks
        weights_only(df_new_headers) -> takes input from previous method
        '''
        tmp_df = self.df.copy()
        tmp_df_2 = tmp_df.iloc[1::2]
        tmp_df_2 = tmp_df_2.drop('Average', axis = 1) # Remove the average col
        tmp_df_2_t = tmp_df_2.transpose() # transpose to switch column and rows

        return tmp_df_2_t
    
    def individual_df(self, df):
        '''
        Input: df = weights_only
        Function to create a list of dataframes corresponding to each column
        Individual dataframes can be extracted from the returned list for further applications
        '''
        tmp_df = df.copy()
        list_of_df = []
        for names in tmp_df.columns:
            list_of_df.append(tmp_df[names])
        return list_of_df
    
    def long_list_of_values(self, list_of_df):
        '''
        list_of_df from individual_df()
        Takes in a list of dataframes and combines them into one long dataframe
        '''
        list_of_values = list_of_df[0]
        for i in range(1,len(list_of_df)):
            list_of_values = pd.concat([list_of_values, list_of_df[i]], axis=0) # Replace append
        list_of_values = list_of_values.reset_index().drop('index', axis=1)
        return list_of_values

    def dates_only(self, df):
        '''
        df = #ExcelProcessing().rename_headers()
        Create dataframe of just dates
        '''
        tmp_df = df.copy()
        date_df = tmp_df.iloc[0::2].drop('Average',axis=1)
        return date_df.T # return a transposed version
    
    def export_file(self, weights_df, dates_df):
        '''
        Combines the weights df and dates df
        Since they were extracted and transformed similarly
        Each weight value matches the correct row within dates
        '''
        export_df = pd.concat([dates_df.reset_index(drop=True),
                                weights_df.reset_index(drop=True)], axis = 1)
        export_df.columns = ['Date', 'Weight']

        return export_df
    
    def rolling_mean_fill_na(self, df, date_value):
        '''
        Fills NA value with the 7 day rolling mean if weights are missing

        df from export_df
        date_value of str type -> example: '2022-05-21' YYYY-mm-dd
        '''
        tmp_df = df.copy()

        idx = tmp_df.index[tmp_df['Date']==date_value].values[0] + 1 # +1, assumes input date is filled
        subset_tmp_df = tmp_df[:idx]
        # Rolling mean over 7 days to fill NA where they appear
        subset_tmp_df.loc[subset_tmp_df['Weight']==None,
                    'Weight'] = pd.Series(subset_tmp_df['Weight']).rolling(7, min_periods=1).mean()
        
        return subset_tmp_df
    
    def create_averages(self, df):
        tmp_df = df.copy()
        tmp_df['Weight'] = tmp_df['Weight'].astype(np.float32)
        tmp_df['fillWeight'] = tmp_df['Weight']
        tmp_df['fillWeight'] = tmp_df['fillWeight'].interpolate()
        tmp_df['MA'] = tmp_df['fillWeight'].rolling(window=7).mean()
        indexer = str(datetime.date.today())
        df_indexer = tmp_df.index[tmp_df['Date']==indexer].values[0] + 1 
        df_subset = tmp_df[:df_indexer]
        return df_subset
                                

def prompt_filepath(source_data, default=''):
    i = 0
    while i == 0:
        if source_data=='export':
            msg = f"\nPlease copy and paste the folder path where the finished results should be exported and press enter"
        else:
            msg = f"\nPlease copy and paste the folder path where {source_data} data sits and press enter"
        print(msg)

        prompt_path = input()
        print(f'\nChecking if input path is valid')
        if os.path.exists(prompt_path):
            print('Found the path')
            i += 1
        else:
            print("Could not find path specified\n")
    return prompt_path

def main(args):
    print(args)

    # get args
    default_path = ''
    data_path = prompt_filepath('weight data', default_path)
    export_path = prompt_filepath('export')
    data_name = args.file_name
    sheet_name = args.sheet_name

    date_value = datetime.date.today() # Always take latest date


    # Load data
    df = pd.read_excel(data_path+'/'+data_name, sheet_name=sheet_name, engine='openpyxl')
    start = time.time()

    # Load and process date
    excel_date = ExcelProcessing(df)
    excel_step_1 = excel_date.drop_columns()
    excel_step_2 = excel_date.rename_headers(excel_step_1)

    # Do weight processing
    weight_convert = WeightConverter(excel_step_2)
    weight_convert_1 = weight_convert.weights_only()
    weight_convert_2 = weight_convert.individual_df(weight_convert_1)
    weight_convert_3 = weight_convert.long_list_of_values(weight_convert_2)

    # Do date processing
    date_convert = weight_convert.dates_only(excel_step_2)
    date_convert_2 = weight_convert.individual_df(date_convert)
    date_convert_3 = weight_convert.long_list_of_values(date_convert_2)

    # Merge weights and dates 
    export_df = weight_convert.export_file(weight_convert_3, date_convert_3)

    averaged_export = weight_convert.create_averages(export_df)
    # Fill na with rolling mean if desired, else NA
    #export_df_2 = weight_convert.rolling_mean_fill_na(export_df, date_value)

    export_fname = f'formatted_weight_{date_value}.csv'
    full_path = os.path.join(export_path, export_fname)
    averaged_export.to_csv(full_path, index=False)
    #export_df_2.to_csv(full_path, index=False) # If NA's want to be filled
    end = time.time()
    print(f"Runtime: {end-start} s")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Tool to convert weight data to proper format')
    parser.add_argument('file_name', help='File name <required>', default='.xlsx')
    parser.add_argument('sheet_name', help='sheet name to extract', nargs='?', default='All')
    
    args, unknown = parser.parse_known_args()

    main(args)
