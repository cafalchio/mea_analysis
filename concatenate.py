import numpy as np
import os
from tqdm.auto import tqdm
from glob import glob
import logging
import shutil

logging.basicConfig(level=logging.DEBUG)


def concatenate(data_path, save_path, amp_names, DEBUG=False):
    """Function that connects part of intan files in different subfolders into a new folder"""
    print(f"{'-'*60}")
    print(f"Concatenating files from: {data_path}")
    # Copy info from the first folder
    try:
        if not os.path.isfile(save_path + "/info.rhd"):
            info = glob(data_path + "/*/info.rhd")[0]
            shutil.copyfile(info, save_path + "/info.rhd")
    except:
        pass  # Expecting that one of the 64 infos will be copied

    for filename in tqdm(amp_names):
        if DEBUG:
            logging.debug(f"FILE : {path}")

        try:
            for i, path in enumerate(sorted(glob(data_path + "/*/"))):
                part_name = path + filename
                if i == 0:
                    temp_name = save_path + "/" + filename
                try:
                    temp = np.fromfile(part_name, dtype=np.int16)
                except:
                    continue
                if i == 0:
                    with open(temp_name, "wb") as fb:
                        fb.write(temp.astype("int16"))
                else:
                    with open(temp_name, "ab+") as fb:
                        fb.write(temp.astype("int16"))
        except:
            logging.info(f"Failed on {part_name}")
            continue
