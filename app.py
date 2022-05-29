# GUI for my script to process weight data

from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import askopenfile
import time 
import pandas as pd
import numpy as np
import datetime
import os
from tkinter import filedialog
from tkinter.filedialog import askopenfile
from tkinter.filedialog import asksaveasfilename


import convert_excel_weight as cew


ws = Tk()
ws.title('Data processor')
ws.geometry('400x200')
ws.iconbitmap('pepe-2.ico')

df = pd.DataFrame()

def load_data():
    # get args
    sheet_name = 'All'

    file_path = filedialog.askopenfilename()

    # Load data
    global df
    df = pd.read_excel(file_path, sheet_name=sheet_name, engine='openpyxl')
    

def process_data():
    global df
    date_value = datetime.date.today() # Always take latest date

    # Load and process date
    excel_date = cew.ExcelProcessing(df)
    excel_step_1 = excel_date.drop_columns()
    excel_step_2 = excel_date.rename_headers(excel_step_1)

    # Do weight processing
    weight_convert = cew.WeightConverter(excel_step_2)
    weight_convert_1 = weight_convert.weights_only()
    weight_convert_2 = weight_convert.individual_df(weight_convert_1)
    weight_convert_3 = weight_convert.long_list_of_values(weight_convert_2)

    # Do date processing
    date_convert = weight_convert.dates_only(excel_step_2)
    date_convert_2 = weight_convert.individual_df(date_convert)
    date_convert_3 = weight_convert.long_list_of_values(date_convert_2)

    # Merge weights and dates 
    export_df = weight_convert.export_file(weight_convert_3, date_convert_3)

    averaged_export = weight_convert.create_averages(export_df, date_value)
    # Fill na with rolling mean if desired, else NA
    #export_df_2 = weight_convert.rolling_mean_fill_na(export_df, date_value)

    try:
        # with block automatically closes file
        with filedialog.asksaveasfile(mode='w', defaultextension=".csv") as file:
            averaged_export.to_csv(file.name)
    except AttributeError:
        # if user cancels save, filedialog returns None rather than a file object, and the 'with' will raise an error
        print("The user cancelled save")


load_data_btn = Button(ws, text='load data', command=load_data)
load_data_btn.pack(pady=20)

# Process and export
process_data_btn = Button(ws, text='process data', command=process_data)
process_data_btn.pack(pady=20)


ws.mainloop()