from tqdm.auto import tqdm
import numpy as np
from scipy import signal
from read_header import read_header
import os
from glob import glob
import gc

gc.enable()


def downsample(data_path, new_path, final_rate=1000):
    """Function that downsample the files in the path and save to the new_path.
    The final sample rate can be entered as final_rate
    Inputs:
        data_path: path to the data
        new_path: path to save the downsampled data
        final_rate: final sample rate
    Returns:
        None, but creates a new file downsampled to the final_rate
    """
    print(f"{'-'*60}")
    print(f"Downsampling to {final_rate} files from: {data_path}")
    head_file = glob(data_path + "/*info.rhd")
    out_path = os.path.join(data_path, new_path)
    if not os.path.exists(out_path):
        os.makedirs(out_path)
    with open(head_file[0], "rb") as f:
        header = read_header(f)
    sample_rate = int(header["sample_rate"])
    factor = int(sample_rate / int(final_rate))

    for filename in tqdm(sorted(glob(data_path + "/" + "amp*.dat"))):
        new_name = os.path.join(
            out_path,
            os.path.basename(filename).split(".")[-2] + f"_sr_{final_rate}.dat",
        )
        b = np.memmap(filename, dtype="int16") * 0.195  # found on the rhd datasheet
        downSample = signal.decimate(b, factor, ftype="fir")
        fp = np.memmap(
            new_name, dtype="int16", mode="w+", offset=0, shape=downSample.shape
        )
        fp[:] = downSample[:]
        fp.flush()

    return None
