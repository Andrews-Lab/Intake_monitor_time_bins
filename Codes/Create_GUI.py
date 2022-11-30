import PySimpleGUI as sg

def default_values():
    
    default = {}

    # Choose the path of a folder with the .ASC file, so the code can import every
    # file in the folder.
    # There should not be a slash at the end of these folder paths.
    default['Import location'] = "C:/Users/hazza/Desktop/Feeding cages data"
    default['Export location'] = "C:/Users/hazza/Desktop/Feeding cages results"
    
    # Choose what time bins should be analysed.
    # You can also add more numbers into this list, so that more input fields appear
    # in the GUI.
    default['Time bin list'] = [30, 45, 60]
    
    # Choose which types of analysis to include.
    default['Grouped by animal raw'] = True
    default['Grouped by animal']     = True
    default['Grouped by stat']       = True
    
    return(default)

def GUI(default):
    
    # Create a dictionary with the inputs from the GUI.
    inputs = {}
    
    # Create a GUI.
    sg.theme("DarkTeal2")
    time_bins_entries = []
    for i in range(len(default['Time bin list'])):
        time_bins_entries += [sg.Input(default_text=default['Time bin list'][i], 
                              key="Timebin"+str(i), size=(5,1), enable_events=True)]
    layout = [
        [sg.T("")], [sg.Text("Choose a folder for the import location"),
                      sg.Input(default_text=default['Import location'],
                               key="Import", enable_events=True),
                      sg.FolderBrowse(key="Import2")],
        [sg.T("")], [sg.Text("Choose a folder for the export location"),
                      sg.Input(default_text=default['Export location'],
                               key="Export", enable_events=True),
                      sg.FolderBrowse(key="Export2")],
        [sg.T("")], [sg.Text("Time bins to analyse (mins)"), *time_bins_entries], [sg.T("")], 
        [sg.Checkbox("Create raw excel sheets grouped by stat", 
                     key="Raw", default=default['Grouped by animal raw'])],
        [sg.Checkbox("Create organised excel sheets grouped by animal", 
                     key="Each animal", default=default['Grouped by animal'])],
        [sg.Checkbox("Create organised excel sheets grouped by stat", 
                     key="Each stat", default=default['Grouped by stat'])],
        [sg.T("")], [sg.Button("Submit")]
              ]
    window = sg.Window('Telemetry analysis', layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event=="Exit":
            window.close()
            sys.exit()
        elif event == "Submit":
            inputs['Import location']   = values["Import"]
            inputs['Export location']   = values["Export"]
            inputs['Time bin list']     = [float(values["Timebin"+str(i)]) 
                                           for i in range(len(default['Time bin list']))
                                           if values["Timebin"+str(i)] != '']
            inputs['Overall sheet']     = values["Raw"]
            inputs['Grouped by animal'] = values["Each animal"]
            inputs['Grouped by stat']   = values["Each stat"]
            window.close()
            break
        
    return(inputs)
