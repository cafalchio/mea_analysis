from csv import field_size_limit
import os
import pandas as pd
import numpy as np
from glob import glob


def input_treatment_times(df_path, slice):

    """Read treatment times and process fo plot

    Input:
        (df):dataframe with times and treatment
        (str):string of slice name
    Returns:
        list of treatment times
        list of treatment names
    """
    all_treats = [
        "normal",
        "modified",
        "change_position",
        "RO",
        "NVP",
        "0Mg",
        "Levetiracetam",
        "perapanel",
        "4-AP",
        "C10",
        "DPH",
    ]
    df = pd.read_csv(df_path)
    clean_t = df.loc[df.slice == slice].dropna(axis=1)
    clean_t = clean_t[[x for x in clean_t.columns if x in all_treats]]
    treats_list = list(clean_t.columns)
    t_times_list = [
        i if type(i) == str else str(i) for col in clean_t.columns for i in clean_t[col]
    ]
    t_times_list = [x.split() for x in t_times_list]
    treats_list = [len(x) * [treat] for x, treat in zip(t_times_list, treats_list)]
    times = sum(t_times_list, [])
    times = [int(float(i)) for i in times]

    return [times, sum(treats_list, [])]


def read_channel(filename):
    """Read the channel from the file name
    Inputs: filename(str): name of the file
    Returns: channel(str): channel name"""
    data_ch = np.fromfile(filename, dtype=np.int16)
    data_ch = data_ch[:]
    return data_ch.copy()


def find_eeg_files(data_path):
    """
    Return the list of files to be plotted
    Inputs:
        path_to_data(str): path from where the eeg files are
    Return:
        files(list): List of files to be plotted
    """

    # print(data_path + f"/amp-{amp}*sr_1000.dat")

    files = sorted(glob(data_path + "/amp-*.dat"))
    print(field_size_limit)
    return files


def get_head():
    """provide the head of the output"""
    print(f"{'-'*60}")
    print(f"\tData Processing Script - Mark Cunninghan's Lab")
    print(f"\t  Matheus Cafalchio - maolivei@tcd.ie - 2022")
    print(f"{'-'*60}")
    return None


def get_amplifiers():
    """Get the list of amplifiers
    Returns:
        list of amplifiers
    """
    # Create file names
    ampA = [f"amp-A-00{i}.dat" for i in range(0, 10)] + [
        f"amp-A-0{i}.dat" for i in range(10, 64)
    ]
    ampB = [f"amp-B-00{i}.dat" for i in range(0, 10)] + [
        f"amp-B-0{i}.dat" for i in range(10, 64)
    ]
    ampC = [f"amp-C-00{i}.dat" for i in range(0, 10)] + [
        f"amp-C-0{i}.dat" for i in range(10, 64)
    ]
    ampD = [f"amp-D-00{i}.dat" for i in range(0, 10)] + [
        f"amp-D-0{i}.dat" for i in range(10, 64)
    ]
    time = ["time.dat"]
    auxA = [f"aux-A-AUX{i}.dat" for i in range(0, 4)]
    auxB = [f"aux-B-AUX{i}.dat" for i in range(0, 4)]
    auxC = [f"aux-C-AUX{i}.dat" for i in range(0, 4)]
    auxD = [f"aux-D-AUX{i}.dat" for i in range(0, 4)]

    amplifiers = {
        "A": [ampA, auxA, time],
        "B": [ampB, auxB, time],
        "C": [ampC, auxC, time],
        "D": [ampD, auxD, time],
    }
    return amplifiers

def get_seizures(log_path, slice_name):
    """
    Read the seizures from the log file
    Inputs:
        log_path(str): path to the log file
        slice_name(str): name of the slice
    Returns:
        seizures(list): list of seizures
    """
    log_file = log_path + f"/{slice_name}.log"
    with open(log_file, "r") as f:
        lines = f.readlines()
    seizures = [line.split() for line in lines]
    seizures = [
        [int(float(i)) for i in seizure] for seizure in seizures if len(seizure) > 1
    ]
    return seizures
    filename = os.path.join(log_path, f"{slice_name}.csv")
    return pd.read_csv(filename)