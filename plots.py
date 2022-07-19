import os
import numpy as np
from tqdm.auto import tqdm
import matplotlib.pyplot as plt
import seaborn as sns
import gc
from utils import *


def plot_LFP(data_path, save_path, df_path, slice_name):
    """Plot data with colors for each treatment

    Inputs:
        data_path (str): path to the data
        save_path (str): path to save the plots
        amp_names (list): list of amplifier files
        df_path (str): path of the treatment_times.csv
        experiment_name (str): experiment_name, related to the row on .csv file

    Returns:
        None
    """
    print(f"{'-'*60}")
    print(f"Plotting downsampled files from: {data_path}")

    if not os.path.exists(save_path):
        os.makedirs(save_path)
    sf = 1000
    treatments = input_treatment_times(df_path, slice_name)
    files = find_eeg_files(data_path)

    for i, file in enumerate(tqdm(files)):
        save_name = save_path + "/" + file[-22:-4]
        try:
            data = read_channel(file)
            colors = {
                "normal": "green",
                "modified": "red",
                "perapanel": "blue",
                "RO": "yellow",
                "NVP": "brown",
                "0Mg": "purple",
                "Levetiracetam": "orange",
                "4-AP": "olive",
                "C10": "gray",
                "DPH": "navajowhite",
            }

            sns.set(font_scale=1.2)
            # Define sampling frequency and time vector
            time = np.arange(data.size) / sf
            fig, ax = plt.subplots(figsize=(20, 4))
            ax.plot(time, data, lw=1.5, color="k")
            if len(treatments[0]) > 0:
                treatments[0] = [x * sf * 60 for x in treatments[0]]
                treatments[0], treatments[1] = zip(
                    *sorted(zip(treatments[0], treatments[1]))
                )
                treatments[0], treatments[1] = list(treatments[0]), list(treatments[1])
                treatments[0].append(time.size - 1)
                for i in range(len(treatments[1])):
                    ax.axvspan(
                        time[treatments[0][i]],
                        time[treatments[0][i + 1]],
                        label=treatments[1][i],
                        color=colors[treatments[1][i]],
                        alpha=0.1,
                    )
            ax.set_xlabel("Time (seconds)")
            ax.set_ylabel("uV")
            # ax.set_title(title)
            ax.set_xlim([time.min(), time.max()])
            if len(treatments[0]) > 0:
                plt.legend(loc="upper right")
            sns.despine(fig)
            plt.savefig(f"{save_name}.jpg", bbox_inches="tight")
            plt.close(fig)
            gc.collect()
        except:
            print(f" Could not plot {file}")
