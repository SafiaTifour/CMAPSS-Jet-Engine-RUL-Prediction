import pandas as pd
from glob import glob

# --------------------------------------------------------------
# Read single txt file
# --------------------------------------------------------------
file = pd.read_csv('../../data/raw/CMAPSSData/RUL_FD001.txt', sep=' ')

# --------------------------------------------------------------
# List all data in data/raw/CMAPSSData
# --------------------------------------------------------------

files = glob('../../data/raw/CMAPSSData/*.txt')

# --------------------------------------------------------------
# function to organize all the data into one single dataframe
# --------------------------------------------------------------



data_frames = {
    "FD001": pd.DataFrame(),
    "FD002": pd.DataFrame(),
    "FD003": pd.DataFrame(),
    "FD004": pd.DataFrame(),
}

columns = [
    "unit_number",
    "time_cycles",
    "op_setting_1",
    "op_setting_2",
    "op_setting_3",
    "sensor_measurement_1",
    "sensor_measurement_2",
    "sensor_measurement_3",
    "sensor_measurement_4",
    "sensor_measurement_5",
    "sensor_measurement_6",
    "sensor_measurement_7",
    "sensor_measurement_8",
    "sensor_measurement_9",
    "sensor_measurement_10",
    "sensor_measurement_11",
    "sensor_measurement_12",
    "sensor_measurement_13",
    "sensor_measurement_14",
    "sensor_measurement_15",
    "sensor_measurement_16",
    "sensor_measurement_17",
    "sensor_measurement_18",
    "sensor_measurement_19",
    "sensor_measurement_20",
    "sensor_measurement_21"
]

data = pd.DataFrame()

def read_data_from_data_files(files, data):

    for file in files:
        with open(file, 'r') as f:
            if "test" in file:
                df = pd.read_table(f, sep='\s+', header=None, names=columns)
                data_frames[file.split("_")[1].split(".")[0]] = pd.concat([data_frames[file.split("_")[1].split(".")[0]], df], ignore_index=True)

    # Concatenate all dataframes into one
    for key in data_frames:
        data_frames[key]["category"] = key
        data = pd.concat([data, data_frames[key]], ignore_index=True)

    for file in files:
        with open(file, 'r') as f:
            if "RUL" in file:
                df = pd.read_table(f, sep='\s+', header=None, names=["RUL"])
            
                for i in range(len(df)):
                    # Extract the category from the filename
                    category = file.split("_")[1].split(".")[0]

                    # Create a boolean mask
                    mask = (data["category"] == category) & (data["unit_number"] == i+1)

                    # Assign the value to the 'RUL' column for the rows that match the mask
                    data.loc[mask, "RUL"] = df.iloc[i]["RUL"]

    return data


data = read_data_from_data_files(files, data)
data.to_pickle("../../data/interim/01_data_processed.pkl")