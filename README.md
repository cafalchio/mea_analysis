## Preprocessing and analysis of Multi Electrode Recordings from Human Slices
<br>

### Intro
<br>


### Methodology

<p align="center">
<img src="https://github.com/cafalchio/mea_analysis/blob/main/mea.png?raw=true" width="400" height="400" >
</p>

### How to use
<br>
The pipeline can be configured using config.ini, each preprocessing step can be added or remove from the pipeline by changing the 'run' parameter to True or False. 
for each step, few configurations need to be added.

**concatenate**


This preprocess step is required for some experiments where the raw recording was broken in several folders during recording to reduce filesize. The script will get each piece of each channel from each folder and connect them in sequence to form a single recording channel file.


Parameters: 
    run : True or False -> run or not the step
    data_path : base path where the subfolders are the data
    save_path : where the files will be saved
    amp : select the amplifier group
    DEBUG : True or False -> on or off the debug prints

**single_file**


This step was created to transform the 64 binary channels into a single channel to be clustered using Spyking Circus (github.com/spyking-circus/spyking-circus). 


Parameters:
    run : True or False -> run or not the step
    data_path : path to the data
    save_path : where the files will be saved
    amp : select the amplifier group
    chunk_sz : 64, 128, 256, 512 etc chunks to process data (optimize for speed)
    DEBUG : True or False -> on or off the debug prints

**Downsample**


Used to represent the LFP. The data is filtered using an 30 point FIR filter with Hamming window and than downsampled.


Parameters:
    run : True or False -> run or not the step
    data_path : path to the data
    final_rate : the final sample rate
    save_path = path that will be created inside the data path


**plot_lfp**


Used to plot the entire recording of each channel. By default the plot will use a 'treatment_times.csv' file that contain the number in minutes of when each treatment was added to the slice.


    run : True or False -> run or not the step
    data_path :  path to the data
    save_path : where the plots will be saved
    slice_name : slice name correspondent to the CSV row
    df_path : path to the csv file containing the treatment times in minutes


### Requirements

matplotlib==3.5.1
numpy==1.22.3
pandas==1.4.2
scipy==1.8.0
seaborn==0.11.2
tqdm==4.64.0



