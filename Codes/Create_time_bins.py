import pandas as pd
import numpy as np
import os

# Define functions for grouping data into time bins.
def find_sum(list1):
    #if (list1 is None or len(list1) == 0):
    if list1 in [None, np.nan, []]:
        return(0)
    else:
        return(sum(list1))
def find_last(list1):
    #if (list1 is None or len(list1) == 0):
    if list1 in [None, np.nan, []]:
        return(np.nan)
    else:
        return(list1[-1])
def find_lights(list1):
    #if (list1 is None or len(list1) == 0):
    if list1 in [None, np.nan, []]:
        return(np.nan)
    elif len(set(list1)) != 1 and 1 in list1:
        return('Transition')
    elif list1[0] == 1:
        return('Dark')
    elif list1[0] > 1:
        return('Light')
    else:
        return('Unknown')
# Define a function for creating a datetime column with the time bin intervals.
def datetime(start_time,float_index):
    def add(val,time):
        return(val+time)
    date_time_col = pd.Series(list(float_index))
    date_time_col = date_time_col.apply(pd.to_timedelta, unit='m')
    date_time_col = date_time_col.apply(add, time=start_time)
    date_time_col = date_time_col.apply(pd.to_datetime).dt.round('1s')
    return(date_time_col)
# Define functions for color coding.
def transition_color(index):
    return('background-color: %s' % 'lightgrey')
def dark_color(index):
    return('background-color: %s' % 'darkgrey')
# Define function for applying color coding.
def color_code(df_export):
    transition_indices = df_export[df_export['Light/dark phase'] == 'Transition'].index
    dark_indices       = df_export[df_export['Light/dark phase'] == 'Dark'].index
    df_export = df_export.style.applymap(transition_color,subset=pd.IndexSlice[transition_indices,'Date and time'])\
                               .applymap(dark_color,subset=pd.IndexSlice[dark_indices,'Date and time'])
    return(df_export)

def prepare_data_for_time_binning(inputs):
    
    # Prepare the data for time binning.

    # Import the excel file and rename columns.
    inputs['Import destination'] = os.path.join(inputs['Import location'], inputs['Filename'])
    df = pd.read_excel(inputs['Import destination'], sheet_name='PSC by period', skiprows=range(8))
    rename_columns = {'Period Start': 'Time', 'Bout\nGrams': 'Bout food weight (grams)',
                      'Bouts': 'Bout frequency', 'Bout\nSeconds': 'Bout duration (secs)',
                      'Lights': 'Light/dark phase', 'PSC': 'Animal numbers'}
    df = df.rename(columns=rename_columns)
    
    # Create a master file.
    # Create many of the above dataframes for each animal.
    inputs['Animals list'] = df['Animal numbers'].unique()
    inputs['Stats list'] = ['Bout food weight (grams)','Bout frequency','Bout duration (secs)']
    master = {}
    master['Each animal (raw)'] = {}
    for animal in inputs['Animals list']:
        master['Each animal (raw)'][animal] = df[df['Animal numbers']==animal]
    
    # Remove unnecessary columns.
    columns_to_use = ['Time', 'Bout food weight (grams)', 'Bout frequency', 
                      'Bout duration (secs)', 'Light/dark phase', 'Animal numbers']
    df = df[columns_to_use]
    
    return(master, df, inputs)

def find_time_bins(df, inputs):

    df_bins = df.copy()
    
    # Add a time column with the minutes since the start time.
    for i in range(len(df_bins)):
        df_bins.at[i,"Time (mins)"] = (df_bins.at[i,"Time"]-df_bins.at[0,"Time"]).total_seconds()/60
    start_time = df_bins.at[0,"Time"]

    # Create a list of the time bins.
    duration_mins = (df_bins.at[len(df_bins)-1,"Time"]-df_bins.at[0,"Time"]).total_seconds()/60
    time_bins_labels = list(np.arange(0,duration_mins+inputs['Time bin (mins)'],inputs['Time bin (mins)']))
    time_bins_mins = [-inputs['Time bin (mins)']] + time_bins_labels

    # Add the bins to the dataframe.
    df_bins['Time bins (mins)'] = pd.cut(df_bins['Time (mins)'], time_bins_mins,
                                         labels=time_bins_labels, right=True)

    # Group the data into time bins. At each bin, list all the values for pellet
    # count for example.
    df_bins = df_bins.drop(columns=['Time (mins)'])
    df_bins = df_bins.groupby(["Animal numbers", "Time bins (mins)"]).agg(list)

    # For each bin, find the sum if it is locomotor activity, average if it is
    # temperature data or last value for the time stamps.
    sum_cols = ['Bout food weight (grams)','Bout frequency','Bout duration (secs)']
    for col in sum_cols:
        df_bins[col] = df_bins[col].apply(find_sum)
    df_bins["Light/dark phase"] = df_bins["Light/dark phase"].apply(find_lights)
    df_bins["Light/dark phase"] = df_bins["Light/dark phase"].fillna(method="ffill")
    df_bins["Time"] = df_bins["Time"].apply(find_last)
    df_bins["Time"] = df_bins["Time"].fillna(method="ffill")
    df_bins = df_bins.rename(columns={"Time": "Date and time"})
    # Convert the multiindex of animal numbers and time bins (mins) into columns.
    df_bins = df_bins.reset_index()
    df_bins["Date and time"] = datetime(start_time, df_bins["Time bins (mins)"])
    # Reorder the columns.
    new_order = ['Date and time', 'Light/dark phase', 'Time bins (mins)', 
                 'Bout food weight (grams)', 'Bout frequency',	
                 'Bout duration (secs)', 'Animal numbers']
    df_bins = df_bins[new_order]
    
    return(df_bins)

def split_data_into_different_sheets(master, df_bins, inputs):
    
    master[inputs['Time bin (mins)']] = {}
    
    # Create a summary of all the stats for each animal.
    animals_list = df_bins['Animal numbers'].unique()
    master[inputs['Time bin (mins)']]['Each animal'] = {}
    for animal in inputs['Animals list']:
        df_each_animal = df_bins[df_bins['Animal numbers']==animal]
        df_each_animal = df_each_animal.drop(columns=['Animal numbers'])
        master[inputs['Time bin (mins)']]['Each animal'][animal] = df_each_animal.copy()
        
    # Create a summary of all the animals for each stat.
    master[inputs['Time bin (mins)']]['Each stat'] = {}
    for stat in inputs['Stats list']:
        df_each_stat = pd.DataFrame()
        for animal in inputs['Animals list']:
            new_col = df_bins[df_bins['Animal numbers']==animal][stat]
            new_col.name = animal
            new_col.index = range(len(new_col))
            df_each_stat = pd.concat([df_each_stat, new_col], axis=1)
        info_stats = ['Date and time', 'Light/dark phase', 'Time bins (mins)']
        info_cols  = df_bins[df_bins['Animal numbers']==animals_list[0]][info_stats]
        df_each_stat = pd.concat([info_cols, df_each_stat], axis=1)
        df_each_stat.index = range(len(df_each_stat))
        # Save the dataframe that shows the data for one stat for many animals.
        master[inputs['Time bin (mins)']]['Each stat'][stat] = df_each_stat.copy()
        
    return(master)

def export_data(master, inputs):
    
    # Export the data into multiple sheets.
    
    if inputs['Overall sheet'] == True:
        # Export the raw dataframes.
        export_name = (str(inputs['Filename']) + ' analysed (overall).xlsx')
        export_destination = os.path.join(inputs['Export location'], export_name)
        with pd.ExcelWriter(export_destination) as writer:
            for animal in inputs['Animals list']:
                df_export = master['Each animal (raw)'][animal]
                df_export.to_excel(writer, sheet_name='Animal '+str(animal), engine='openpyxl', index=False)   
    
    for inputs['Time bin (mins)'] in inputs['Time bin list']:
        
        if inputs['Grouped by animal'] == True:
            # Export the individual animal dataframes.
            export_name = (str(inputs['Filename']) + ' analysed (' + str(int(inputs['Time bin (mins)'])) + 
                           ' min time bins' + ' grouped by animal).xlsx')
            inputs['Export destination'] = os.path.join(inputs['Export location'], export_name)
            with pd.ExcelWriter(inputs['Export destination']) as writer:
                for animal in inputs['Animals list']:
                    df_export = master[inputs['Time bin (mins)']]['Each animal'][animal]
                    df_export = color_code(df_export) # Colour code the dark and transition (between light and dark) times.
                    df_export.to_excel(writer, sheet_name='Animal '+str(animal), engine='openpyxl', index=False)         
        
        if inputs['Grouped by stat'] == True:
            # Export the individual stat dataframes.
            export_name = (str(inputs['Filename']) + ' analysed (' + str(int(inputs['Time bin (mins)'])) + 
                           ' min time bins' + ' grouped by stat).xlsx')
            inputs['Export destination'] = os.path.join(inputs['Export location'], export_name)
            with pd.ExcelWriter(inputs['Export destination']) as writer:
                for stat in inputs['Stats list']:
                    df_export = master[inputs['Time bin (mins)']]['Each stat'][stat]
                    df_export = color_code(df_export) # Colour code the dark and transition (between light and dark) times.
                    df_export.to_excel(writer, sheet_name=str(stat), engine='openpyxl', index=False)  
