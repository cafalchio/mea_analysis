from create_single_file import single_file
from concatenate import concatenate
from downsample import downsample
from utils import *
from plots import plot_raster, plot_spikes_around_seizure, plot_waveforms, plot_LFP
from configparser import ConfigParser
import time


file = "config.ini"
config = ConfigParser()
config.read(file)


def main():
    """Run the main function"""
    st = time.time()
    _ = get_head()
    amplifiers = get_amplifiers()
    # Run concatenate files from multiple folders
    if config["concatenate"]["run"] == "True":
        data_path = config["concatenate"]["data_path"]
        save_path = config["concatenate"]["save_path"]
        amp = config["concatenate"]["amp"]
        for amp_names in amplifiers[amp]:
            concatenate(data_path, save_path, amp_names)

    # Run create single file for clustering
    if config["single_file"]["run"] == "True":
        data_path = config["single_file"]["data_path"]
        save_path = config["single_file"]["save_path"]
        amp = config["single_file"]["amp"]
        chunk_sz = int(config["single_file"]["chunk_sz"])
        amp_names = amplifiers[amp][0]
        single_file(data_path, amp_names, save_path, chunk_sz)

    # Run downsampling files
    if config["downsample"]["run"] == "True":
        data_path = config["downsample"]["data_path"]
        save_path = config["downsample"]["save_path"]
        final_rate = config["downsample"]["final_rate"]
        downsample(data_path, save_path, final_rate)

    # Run plotting LFP with treatments
    if config["plot_lfp"]["run"] == "True":
        data_path = config["plot_lfp"]["data_path"]
        save_path = config["plot_lfp"]["save_path"]
        df_path = config["plot_lfp"]["df_path"]
        slice_name = config["plot_lfp"]["slice_name"]
        plot_LFP(data_path, save_path, df_path, slice_name)

    # Run after clustering spikes_plots plots
    if config["spikes_plots"]["run"] == "True":
        data_path = config["spikes_plots"]["data_path"]
        save_path = config["spikes_plots"]["save_path"]
        if config["spikes_plots"]["plot_raster"] == "True":
            plot_raster(data_path, data=None, save_path=save_path, save_name="raster")
        if config["spikes_plots"]["plot_waveforms"] == "True":
            plot_waveforms(data_path, save_path, save_name="waveforms")

    # Open seizure data
    if config["seizures"]["run"] == "True":
        csv_path = config["seizures"]["csv_path"]
        slice_name = config["seizures"]["slice_name"]
        position = config["seizures"]["position"]
        seizure_times = get_seizures(csv_path, slice_name, position)
        spike_times = get_spike_times(data_path)
        plot_spikes_around_seizure(
            spike_times, seizure_times, save_path=None, save_name="raster"
        )

    et = time.time()
    # get the execution time
    elapsed_time = et - st
    print(f"Execution time: {int(elapsed_time)} seconds")


if __name__ == "__main__":
    main()
    print("Done!")
