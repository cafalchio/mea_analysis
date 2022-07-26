import os
import numpy as np
from tqdm.auto import tqdm
import matplotlib.pyplot as plt
import seaborn as sns
import gc
from utils import *
from phylib.io.model import load_model


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


def plot_raster(data_path, data=None, save_path=None, save_name="raster"):
    """Plot all waveforms
    Inputs:
        data_path(str):
            path to the data GUI
        spk_times(str):
            path to the params.py file
        spk_clusters(str):
            path to spike_clusters file
        clusters_info(str):
            path to the clusters_info file
        data(np.array):
            data to align the raster plot, usually LFP data
        save_to:
            name or path of the fig to be saved

    Returns:
        None
    """
    print("Plotting Raters..")
    # data path files
    spike_times = data_path + "spike_times.npy"
    spike_clusters = data_path + "spike_clusters.npy"
    clusters_info = data_path + "cluster_info.tsv"
    # load spike times
    spike_times = np.load(spike_times)
    # Load spike clusters
    spike_clusters = np.load(spike_clusters)
    # load cluster info
    clusters = pd.read_csv(clusters_info, delimiter="\t")
    clusters = clusters.loc[clusters.group == "good"].cluster_id.values
    n_figs = len(clusters)
    f, axes = plt.subplots(n_figs, figsize=(20, 1 * n_figs))
    for i, cluster_id in enumerate(clusters):
        # We get the waveforms of the cluster.
        unit_spikes = spike_times[spike_clusters == cluster_id]
        axes[i].eventplot(unit_spikes, data=data)
        if data:
            axes[i].set_xlim(0, data.size)
        axes[i].get_yaxis().set_visible(False)
        axes[i].get_xaxis().set_visible(False)
        axes[i].spines["top"].set_visible(False)
        axes[i].spines["right"].set_visible(False)
        axes[i].spines["left"].set_visible(False)
        axes[i].spines["bottom"].set_visible(False)

    if save_path is not None:
        plt.savefig(save_path + save_name)
    else:
        plt.show()
    pass


def plot_waveforms(data_path, save_path=None, save_name="raster"):
    """Plot all waveforms
    Inputs:
        params(str):
            path to the params.py file
        cluster_info(str):
            path to the clusters_info file
        save_to:
            name or path of the fig to be saved

    Returns:
        None
    """
    print("Plotting Waveforms..")
    # load files
    clusters_info = data_path + "cluster_info.tsv"
    params = data_path + "params.py"
    # load phy model
    model = load_model(params)
    # We obtain the cluster id from the command-line arguments.
    clusters_info = pd.read_csv(clusters_info, delimiter="\t")
    clusters = clusters_info.loc[clusters_info.group == "good"].cluster_id.values

    n_figs = len(clusters)
    n_channels_loc = 2
    if n_figs == 0:
        print("No figures")
        return None

    f, axes = plt.subplots(n_figs, min(4, n_channels_loc), figsize=(2, 1 * n_figs))
    for i, cluster_id in enumerate(clusters):

        # We get the waveforms of the cluster.
        waveforms = model.get_cluster_spike_waveforms(cluster_id)
        n_spikes, n_samples, _ = waveforms.shape
        channel_ids = model.get_cluster_channels(cluster_id)
        for ch in range(min(2, n_channels_loc)):
            axes[i, ch].plot(waveforms[::50, :, ch].T, c="royalblue", alpha=0.3)
            axes[i, ch].plot(waveforms[::50, :, ch].T.mean(axis=1), c="blue", alpha=0.5)
            axes[i, ch].get_yaxis().set_visible(False)
            axes[i, ch].get_xaxis().set_visible(False)
            # axes[i, ch].set_title(f'Ch {channel_ids}')
            # axes[i, ch].text(45,160, f'{spk_rate}Hz', fontdict=None)
            axes[i, ch].spines["top"].set_visible(False)
            axes[i, ch].spines["right"].set_visible(False)
            axes[i, ch].spines["left"].set_visible(False)
            axes[i, ch].spines["bottom"].set_visible(False)

    if save_path:
        print("savepath")
        plt.savefig(save_path + save_name + ".jpg")
    # else:
    #     plt.show()
    # pass
