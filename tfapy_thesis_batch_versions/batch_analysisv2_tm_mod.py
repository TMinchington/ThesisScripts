import argparse
import pandas as pd
from tfa_lib import wavelets as wl
import numpy as np
import os

def perform_wavelet_analysis_on_file(input_file):
    '''Performs wavelet analysis on the specified data frame. Will generate output files containing the
    wavelet spectrum and the periods.
    
    Parameters:
    -----------
    
    input_file : string
        path to an excell spread sheet. Time course data from single cells must be saved in different
        columns of the file
        
    Returns:
    --------
    
    nothing : Files writes wavelet analysis to files.
    '''
    
    # define parameters
    # sinc_cutoff = 1000.0
    sampling_interval = args.sampling_interval
    # max_period = 1000
    min_period = 60
    number_periods = 1000
    # period_range = np.linspace(min_period, max_period, number_periods)
    ridge_power_threshold = 0.0 # only power values above this number may be considered 'on the ridge'
    enable_ridge_smoothing = False
    size_of_smoothing_window = 0 # in number of timepoints

    folder_name = os.path.dirname(input_file)

    extension = '.' + input_file.split('.')[-1]
    # print(os.path.join(folder_name, input_file.replace(extension, '_data'), 'wavelet'))
    # exit()
    if not os.path.isdir(os.path.join(folder_name, input_file.replace(extension, '_data'), 'wavelet')): # creates an output directory for the wavelet data
        
        os.makedirs(os.path.join(folder_name, input_file.replace(extension, '_data'), 'wavelet'))

    if extension != '.xlsx':

        try:

            cell_data_frame = pd.read_csv(input_file)

        except:

            exit(f'Unknown file type: {extension}')

    else:

        cell_data_frame = pd.read_excel(input_file)

    # loop over all cells in file and perform analysis
    all_ridges = pd.DataFrame()
    all_periods = pd.DataFrame()
    all_phases = pd.DataFrame()
    all_powers = pd.DataFrame()
    
    for cell_name in cell_data_frame:

        if 'time' in cell_name.lower():
            continue

        this_signal = cell_data_frame[cell_name]
        this_signal = this_signal[~np.isnan(this_signal)]
        
        if len(this_signal)*sampling_interval < 360:
            continue
            
        print(cell_name)
        print('len of this signal is')
        print(len(this_signal))

        sinc_cutoff = (len(this_signal) * sampling_interval) *.95
        max_period = (len(this_signal) * sampling_interval) *.95
        
        period_range = np.linspace(min_period, max_period, number_periods)

        these_times = np.arange(0,len(this_signal), step = 1) * sampling_interval
        trend = calc_trend(this_signal, sinc_cutoff, sampling_interval)
        detrended_signal = this_signal - trend
        this_power_spectrum, this_wavelet_transform = wl.compute_spectrum(detrended_signal, sampling_interval, period_range)
        this_ridge_indices = wl.get_maxRidge(this_power_spectrum)
        this_ridge_data = wl.make_ridge_data(this_ridge_indices,
                                             this_power_spectrum,
                                             this_wavelet_transform,
                                             period_range,
                                             these_times,
                                             Thresh = ridge_power_threshold, 
                                             smoothing = enable_ridge_smoothing, 
                                             win_len = size_of_smoothing_window)

        this_ridge_data_frame = pd.DataFrame()
        # add everything to data frame
        for key in this_ridge_data:
            this_ridge_data_frame[key] = this_ridge_data[key]            
            long_key = cell_name + '_' + key
            intermediate_data_frame = pd.DataFrame()
            intermediate_data_frame[long_key] = this_ridge_data[key]
            all_ridges = pd.concat([all_ridges, intermediate_data_frame], axis = 1)
#             all_ridges.assign(long_key = pd.Series(this_ridge_data[key]))
#             all_ridges[long_key] = pd.Series(this_ridge_data[key])
            if key == 'periods':
                intermediate_data_frame = pd.DataFrame()
                intermediate_data_frame[long_key] = this_ridge_data[key]
                all_periods = pd.concat([all_periods, intermediate_data_frame], axis = 1)               
            if key == 'phase':
                intermediate_data_frame = pd.DataFrame()
                intermediate_data_frame[long_key] = this_ridge_data[key]
                all_phases = pd.concat([all_phases, intermediate_data_frame], axis = 1)               
            if key == 'power':
                intermediate_data_frame = pd.DataFrame()
                intermediate_data_frame[long_key] = this_ridge_data[key]
                all_powers = pd.concat([all_powers, intermediate_data_frame], axis = 1)               

        # save data
        float_format = '%.2f' # still old style :/
        power_spectrum_file_name = os.path.join(folder_name, input_file.replace(extension, '_data'), 'wavelet','power_spectrum_' + 
                                                cell_name +extension)
        power_spectrum_data_frame = pd.DataFrame(this_power_spectrum)
        power_spectrum_data_frame.to_excel(power_spectrum_file_name, 
                                           index = False,
                                           float_format = float_format)

        ridge_file_name = os.path.join(folder_name, input_file.replace(extension, '_data'), 'wavelet','ridge_' + 
                                                    cell_name +extension)
        this_ridge_data_frame.to_excel(ridge_file_name, 
                                       index = False,
                                       float_format = float_format
                                      )
    

    full_file_name = ridge_file_name = os.path.join(folder_name, input_file.replace(extension, '_data'), 'wavelet', 'all_wavelet_data.xlsx')
    periods_file_name = ridge_file_name = os.path.join(folder_name, input_file.replace(extension, '_data'), 'wavelet','all_periods.xlsx')
    periods_file_name_csv = ridge_file_name = os.path.join(folder_name, input_file.replace(extension, '_data'), 'wavelet','all_periods.csv')
    powers_file_name = ridge_file_name = os.path.join(folder_name, input_file.replace(extension, '_data'), 'wavelet','all_powers.xlsx')
    powers_file_name_csv = ridge_file_name = os.path.join(folder_name, input_file.replace(extension, '_data'), 'wavelet','all_powers.csv')
    phases_file_name = ridge_file_name = os.path.join(folder_name, input_file.replace(extension, '_data'), 'wavelet','all_phases.xlsx')
    all_ridges.to_excel(full_file_name, 
                        index = False,
                        float_format = float_format
                        )
    all_periods.to_excel(periods_file_name, 
                        index = False,
                        float_format = float_format
                        )
    all_periods.to_csv(periods_file_name_csv, 
                        index = False,
                        float_format = float_format
                        )
    all_powers.to_excel(powers_file_name, 
                        index = False,
                        float_format = float_format
                        )
    all_powers.to_csv(powers_file_name_csv, 
                        index = False,
                        float_format = float_format
                        )
    all_phases.to_excel(phases_file_name, 
                        index = False,
                        float_format = float_format
                        )

def calc_trend(signal, cutoff, sampling_interval):
      
    trend = wl.sinc_smooth(raw_signal = signal, T_c = cutoff, dt = sampling_interval)
    return trend

if __name__ == '__main__':
    programtext = 'This is a script to perform wavelet analysis of single-cell time course data in batch'
    parser = argparse.ArgumentParser(description = programtext)
    parser.add_argument('-i','--inputfile', help = 'Specify the input file, needs to be an excel file')
    parser.add_argument('-si','--sampling_interval', default=10, type=int, help = 'Specify the input file, needs to be an excel file')
    
    args = parser.parse_args()
    
    input_file = args.inputfile

    perform_wavelet_analysis_on_file(input_file)
