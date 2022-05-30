# GUI for my script to process weight data
# Ideally we create a class for load_data and process_data
# That way we can handle df within the class rather than calling global

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
import tkinter as tk
from tkinter import ttk

import convert_excel_weight as cew



class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        # Set window attributes
        self.title('Data processor')
        self.geometry('500x500')
        self.iconbitmap('./icons/pepe-2.ico')
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill="both", expand="true")
        self.pack_propagate(False)

        # Set frames for inputs and outputs
        frame_1 = tk.LabelFrame(self, text="Data")
        frame_1.place(height=250, width=500)

        file_frame = tk.LabelFrame(self, text="Load file")
        file_frame.place(height=100, width=400, rely=0.65, relx=0)
        
        self.label_file = ttk.Label(file_frame, text="No File Selected")
        self.label_file.place(rely=0, relx=0)

        # Set TreeView Widget
        self.tv1 = ttk.Treeview(frame_1)
        self.tv1.place(relheight=1, relwidth=1)

        tree_scroll_y = tk.Scrollbar(frame_1, orient="vertical", command=self.tv1.yview)
        tree_scroll_x = tk.Scrollbar(frame_1, orient="horizontal", command=self.tv1.xview)
        self.tv1.configure(xscrollcommand=tree_scroll_x.set, yscrollcommand=tree_scroll_y.set)
        tree_scroll_x.pack(side="bottom", fill="x")
        tree_scroll_y.pack(side="right", fill="y")

        self.df = pd.DataFrame()

    def load_data(self):
        # get args
        sheet_name = 'All'

        file_name = filedialog.askopenfilename(initialdir="/",
                                                title="Select a file",
                                                filetype=(("xlsx files", "*.xlsx"), ("All Files", "*.*")))

        # Load data
        self.label_file["text"] = file_name
        file_path = self.label_file["text"]

        try:
            self.df = pd.read_excel(file_name, sheet_name=sheet_name, engine='openpyxl')
        
        except ValueError:
            tk.messagebox.showerror("Information", "THe file you have chosen is invalid")
            return None
        
        except FileNotFoundError:
            tk.messagebox.showerror("Information", f"No such file as {file_path}")
        
        self.clear_data()
        self.tv1["column"] = list(self.df.columns)
        self.tv1["show"] = "headings"

        # Set column names
        for column in self.tv1["columns"]:
            self.tv1.heading(column, text=column)
        
        df_rows = self.df.to_numpy().tolist()
        for row in df_rows:
            self.tv1.insert("", "end", values=row)

    def clear_data(self):
        self.tv1.delete(*self.tv1.get_children())

    def process_data(self):
        date_value = datetime.date.today() # Always take latest date

        # Load and process date
        excel_date = cew.ExcelProcessing(self.df)
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

def main():
    frame = Application()
    
    load_data_btn = Button(frame, text='load data', command=frame.load_data)
    load_data_btn.place(rely=0.65, relx= 0.5)

    # Process and export
    process_data_btn = Button(frame, text='process data', command=frame.process_data)
    process_data_btn.place(rely=0.65, relx=0.3)

    frame.mainloop()


if __name__ == '__main__':
    main()
    #ws.mainloop()