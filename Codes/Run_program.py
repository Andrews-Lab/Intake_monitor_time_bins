import os
from tqdm import tqdm
from Create_GUI import default_values, GUI
from Create_time_bins import (prepare_data_for_time_binning, find_time_bins, 
                              split_data_into_different_sheets, export_data)

# Run the GUI.
default = default_values()
inputs = GUI(default)

# Analyse the data in each excel file.
import_files = [file for file in os.listdir(inputs['Import location']) if
                (file.endswith(".xlsx") and file.startswith("~$") == False)]

for inputs['Filename'] in tqdm(import_files, ncols=70):

    master, df, inputs = prepare_data_for_time_binning(inputs)
    
    for inputs['Time bin (mins)'] in inputs['Time bin list']:
        
        df_bins = find_time_bins(df, inputs)
        master  = split_data_into_different_sheets(master, df_bins, inputs)
        
    export_data(master, inputs)
    