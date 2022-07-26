from tqdm.auto import tqdm
import numpy as np
import os
import gc
from read_header import read_header
import logging

logging.basicConfig(filename="single.log", level=logging.DEBUG)
gc.enable()

## This script create a single binary file to be used with spyking circus.
# First it completes channels with missing data with zeros in the end.
# The inclusion of zeros could generate error on analysis that requires spike times.
#### CHANGED -> Instead of appending zeros, the channels were removed.


def create_zeros(size, good_channels, data_path, amp_names):
    """This function create zeros file to substitute files that are smaller than the majority
    In the end some of the channels will be just zeros from start to end and can be discarded,
    They are kept here to keed the size 64 channels.

    Inputs:
        size: the size of the file in int16 bytes
        good_channels: the list of channels with that size
        data_path: the path to the data
        amp_names: the list of amp_names
    """
    logging.debug("Function create_zeros")
    for filename in amp_names:
        if filename not in good_channels:
            # filesize = int(os.path.getsize(data_path+filename)/2)
            new_data = np.zeros(size)
            with open(data_path + "/" + filename, "wb") as fb:
                fb.write(new_data.astype("int16"))
    return None


def get_good_channels(data_path, amp_names):
    """
    Returns the size of the file in int16 bytes and the list of channels with that size.
    Inputs:
        data_path: the path to the data
        amp_names: the list of amp_names
    Returns:
        size: the size of the file in int16 bytes
        good_channels: the list of channels with that size
    """
    logging.debug("Function get_good_channels")

    filesize = {}
    for filename in amp_names:
        try:
            filesize[filename] = int(os.path.getsize(data_path + "/" + filename) / 2)
            # sizes.append(int(os.path.getsize(data_path+filename)/2))
        except:
            print(f"{filename} not exist.")
            filesize[filename] = 0
            # np.zeros(max(sizes), dtype=np.int16).tofile(data_path+filename)

    size = max(filesize.values())
    logging.debug(f"\t\t filesize: { max(filesize.values())}")
    if size == 0:
        return 0, None

    good_channels = [key for key in filesize.keys() if filesize[key] == size]
    logging.debug(f"\t\t number good channels: {len(good_channels)}")
    return size, good_channels


def single_file(data_path, amp_names, save_path, chunk_sz=512):
    """Create a NxM he simplest file format is the raw_binary one.
        Suppose you have N channels
        c0,c1,...,cN

        And if you assume that ci(t)
        is the value of channel ci

        at time t, then your datafile should be a raw file with values
        c0(0),c1(0),...,cN(0),c0(1),...,cN(1),...cN(T)

    This is simply the flatten version of your recordings matrix, with size N x T
    returns: bad channels

    Inputs:
        data_path: the path to the data
        amp_names: the list of amp_names
        save_path: the path to save the data
        chunk_sz: the size of the chunk in int16 bytes
    Returns:
        None, creates a new file .dat
    """
    print(f"{'-'*60}")
    print(f"Creating a single file from: {data_path}")
    print("Can take a while ...")

    out_data = save_path + "/" +"".join(data_path.split("/")[-3:]) + ".bin"
    logging.debug(f"Started")
    try:
        info_file = data_path + "/info.rhd"
        logging.debug(f" info file : {info_file}")
        header = read_header(open(info_file, "rb"))
        sample_rate = np.asarray(header["sample_rate"])
        logging.debug(f" sample_rate : {sample_rate}")
        sample_rate.tofile(save_path + f"sample_rate_{int(sample_rate)}.txt")
    except:
        print("Could not determine sample rate")

    logging.debug(f"data path : {data_path}")
    logging.debug(f"amp_names : {amp_names}")
    size, good_channels = get_good_channels(data_path, amp_names)

    if not good_channels:
        logging.debug(f'sample_rate : {amp_names[0].split("-")[1]}')
        print(f'No data in channel {amp_names[0].split("-")[1]}')
        exit(-1)
    create_zeros(size, good_channels, data_path, amp_names)

    if size / chunk_sz > int(size / chunk_sz):
        n = int(size / chunk_sz) + 1
    else:
        n = int(size / chunk_sz)

    logging.debug(f"Start For loop")
    for i in tqdm(range(0, size, n)):
        chunk = np.array(
            [
                np.memmap(data_path + "/" + filename, dtype="int16")[i : i + n]
                for filename in sorted(amp_names)
            ]
        ).T.flatten()

        if i == 0:
            with open(out_data, "wb") as fb:
                fb.write(chunk.astype("int16").tobytes())
        else:
            with open(out_data, "ab+") as fb:
                fb.write(chunk.astype("int16").tobytes())
    print("Done!")
