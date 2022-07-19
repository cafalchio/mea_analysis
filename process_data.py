from create_single_file import single_file
from concatenate import concatenate
from downsample import downsample
from utils import get_amplifiers, get_head
from plots import plot_LFP
from configparser import ConfigParser

file = "config.ini"
config = ConfigParser()
config.read(file)


def main():
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
    if config["plots"]["run"] == "True":
        data_path = config["plots"]["data_path"]
        save_path = config["plots"]["save_path"]
        df_path = config["plots"]["df_path"]
        slice_name = config["plots"]["slice_name"]
        plot_LFP(data_path, save_path, df_path, slice_name)


if __name__ == "__main__":
    main()
    print("Done!")