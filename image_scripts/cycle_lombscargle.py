"""
cycles through statistic files and runs combin outputs and classy track
"""

def perform_and_return_lombs(x, y):

    import numpy as np
    import matplotlib.pyplot as plt
    from scipy import signal
    from astropy.stats import LombScargle

    f = np.linspace(0.01, 3, 10_000)

    lombS = LombScargle(x, y)
    power = lombS.power(f)
    fmax = f[list(power).index(power.max())]
    period =  1/fmax

    pval = lombS.false_alarm_probability(max(list(power)), method='bootstrap')

    return power, f, period, pval, fmax


def perform_and_return_fft(x, y):

    import numpy as np
    import matplotlib.pyplot as plt
    import scipy.fftpack

    # Number of samplepoints
    N = len(y)
    # sample spacing
    T = max(x) / len(x)
    # x = np.linspace(0.0, N*T, N)
    # y = np.sin(50.0 * 2.0*np.pi*x) + 0.5*np.sin(80.0 * 2.0*np.pi*x)
    yf = scipy.fftpack.fft(y)
    xf = np.linspace(0.0, 1.0/(2.0*T), N//2)

    # fig, ax = plt.subplots()
    # ax.plot(xf, 2.0/N * np.abs(yf[:N//2]))
    power = 2.0/N * np.abs(yf[:N//2])
    # plt.show()
    # plt.close()
    fmax = xf[list(power).index(power.max())]
    period = 1/fmax

    return power, f, period, 0, fmax

def calculate_power_spectrum_of_trajectory(trajectory, normalize = True):
    import numpy as np
    '''Calculate the power spectrum, coherence, and period, of a trajectory. 
    Works by applying discrete fourier transformation. We define the power spectrum as the square of the
    absolute of the fourier transform, and we define the coherence as in 
    Phillips et al (eLife, 2016): the relative area of the power spectrum
    occopied by a 20% frequency band around the maximum frequency.
    The maximum frequency corresponds to the inverse of the period.
    The returned power spectum excludes the frequency 0 and thus neglects
    the mean of the signal. The power spectrum is normalised so that all entries add up to one,
    unless normalized = False is specified.
    
    Parameters:
    ---------- 
    
    trajectories : ndarray
        2D array. First column is time, second column contains the signal that is aimed to be analysed.
        
    normalize : bool
        If True then the power spectrum is normalised such that all entries add to one. Otherwise
        no normalization is performed.
    
    Result:
    ------
    
    power_spectrum : ndarray
        first column contains frequencies, second column contains the power spectrum
        |F(x)|^2, where F denotes the Fourier transform and x is the mean signal
        extracted from the argument `trajectories'. The spectrum is normalised
        to add up to one.
    
    coherence : float
        coherence value for this trajectory, as defined by Phillips et al
    
    period : float
        period corresponding to the maximum observed frequency
    '''
    # Calculate power spectrum
    number_of_data_points = len(trajectory)
    interval_length = trajectory[-1,0]
    trajectory_to_transform = trajectory[:,1] - np.mean(trajectory[:,1])
    fourier_transform = np.fft.fft(trajectory_to_transform, norm = 'ortho')
#     fourier_transform = np.fft.fft(trajectory_to_transform)
    fourier_frequencies = np.arange( 0,number_of_data_points/(2*interval_length), 
                                                     1.0/(interval_length) )
    power_spectrum_without_frequencies = np.power(np.abs(fourier_transform[:(number_of_data_points//2)]),2)
    
    # this should really be a decision about the even/oddness of number of datapoints
    try:
        power_spectrum = np.vstack((fourier_frequencies, power_spectrum_without_frequencies)).transpose()
    except ValueError:
        power_spectrum = np.vstack((fourier_frequencies[:-1], power_spectrum_without_frequencies)).transpose()

    power_integral = np.trapz(power_spectrum[1:,1], power_spectrum[1:,0])
    normalized_power_spectrum = power_spectrum[1:].copy()
    normalized_power_spectrum[:,1] = power_spectrum[1:,1]/power_integral
    coherence, period = calculate_coherence_and_period_of_power_spectrum(normalized_power_spectrum)
    if normalize:
        power_spectrum = normalized_power_spectrum

    return power_spectrum, coherence, period

def calculate_coherence_and_period_of_power_spectrum(power_spectrum):
    '''Calculate the coherence and peridod from a power spectrum.
    We define the coherence as in Phillips et al (eLife, 2016) as 
    the relative area of the power spectrum
    occopied by a 20% frequency band around the maximum frequency.
    The maximum frequency corresponds to the inverse of the period.
    
    Parameters 
    ----------
    
    power_spectrum : ndarray
        2D array of float values. First column contains frequencies,
        the second column contains power spectum values at these frequencies.
        
    Results
    -------
    
    coherence : float
        Coherence value as calculated around the maximum frequency band.
        
    period : float
        The inverse of the maximum observed frequency.
    '''
    # Calculate coherence:
    max_index = np.argmax(power_spectrum[:,1])
    max_power_frequency = power_spectrum[max_index,0]
    
    power_spectrum_interpolation = scipy.interpolate.interp1d(power_spectrum[:,0], power_spectrum[:,1])

    coherence_boundary_left = max_power_frequency - max_power_frequency*0.1
    coherence_boundary_right = max_power_frequency + max_power_frequency*0.1

    if coherence_boundary_left < power_spectrum[0,0]:
        coherence_boundary_left = power_spectrum[0,0]

    if coherence_boundary_right > power_spectrum[-1,0]:
        coherence_boundary_right = power_spectrum[-1,0]
        
    first_left_index = np.min(np.where(power_spectrum[:,0]>coherence_boundary_left))
    last_right_index = np.min(np.where(power_spectrum[:,0]>=coherence_boundary_right))
    integration_axis = np.hstack(([coherence_boundary_left], 
                                  power_spectrum[first_left_index:last_right_index,0],
                                  [coherence_boundary_right]))

    interpolation_values = power_spectrum_interpolation(integration_axis)
    coherence_area = np.trapz(interpolation_values, integration_axis)
    full_area = np.trapz(power_spectrum[:,1], power_spectrum[:,0])
    coherence = coherence_area/full_area
    
    # calculate period: 
    period = 1./max_power_frequency
    
    return coherence, period

def test_scargl():
    import matplotlib.pyplot as plt
    import numpy as np

    time = np.arange(0, 30, .1)
    
    y = np.sin(time)

    power, f, period, pval, fmax = perform_and_return_lombs(time, y)

    

    plt.plot(time, y)
    plt.xlabel('Time')
    plt.ylabel('intensity (au)')
    plt.show()
    plt.close() 

    plt.plot(f, power)
    plt.show()
    plt.close()
    tragectory = np.column_stack((time, y))
    print(tragectory)
    power_spectrum, coherence, period_joch = calculate_power_spectrum_of_trajectory(tragectory)
    f = power_spectrum[:, 0]
    power = power_spectrum[:, 1]
    plt.plot(f, power)
    plt.show()
    plt.close()
    print('lomScarg ->>>', period, pval, fmax)
    print('fft ->>>', period_joch, coherence)
    exit()

if __name__ == "__main__":
    
    import argparse
    import os
    import subprocess
    import time
    import pandas as pd
    import numpy as np
    import scipy

    parser = argparse.ArgumentParser()
    parser.add_argument('data_loc', help='data_locations_file')
    parser.add_argument('output_location', help='output directory, a folder called lombResults will be created in this location')
    args = parser.parse_args()
    
    # test_scargl()
    
    data_path = pd.read_csv(args.data_loc, header=0)
    track_spots_sub = data_path[(data_path['spot_type']=='track') & (data_path['stat_type']=='spots')]
    
    # print(track_spots_sub.loc[1])

    lomb_dir = os.path.join(args.output_location, 'lombResults')

    if not os.path.isdir(lomb_dir):
        os.makedirs(lomb_dir)

    master_periods = os.path.join(lomb_dir, 'lombPeriods.tsv')
    master_lomb_traces = os.path.join(lomb_dir, 'lombTraces.tsv')

    master_periods_w = open(master_periods, 'w')
    master_lomb_traces_w = open(master_lomb_traces, 'w')

    master_periods_w.write('gene\tclone\tdate\tposition\tchannel\tinterval\ttrackx\ttrack_len\tfmax\tperiod\tpval\tfoler_path\tfile\tfft_period\tfft_fmax\tcoherrence\n')
    master_lomb_traces_w.write('gene\tclone\tdate\tposition\tpower\tf\tfile\ttrack\tgroup\n')

    for index, row in track_spots_sub.iterrows():
        
        (gene, clone, date, position, stat_type, channel, interval, spot_type, root_path, file_path, background) = row

        folder = os.path.join(root_path, file_path)
        print(folder)

        detrended = os.path.join(folder, 'all_detailed-joined-detrended.tsv')
        detrended_full = os.path.join(folder, 'all_detailed-joined_full_track-detrended.tsv')

        for filex in [detrended]:

            loaded_file = pd.read_csv(filex, header=0, sep='\t')

            loaded_file['file'] = filex

            for trackx in set(loaded_file.track):
                
                track_sub = loaded_file[(loaded_file.track == trackx) & (loaded_file.variable == "Intensity Mean") & (loaded_file.channel == channel)]
                track_sub_no_nan = track_sub.dropna()

                # try:
                    
                #     tragectory = np.column_stack((track_sub_no_nan.hours, track_sub_no_nan.detrended))
                #     power_spectrum, coherence, period_fft = calculate_power_spectrum_of_trajectory(tragectory)
                #     power_fft = power_spectrum[:, 0]
                #     f_fft = power_spectrum[:, 1]
                    
                # except:
                    
                power_fft = 'NAN'
                f_fft = 'NAN'
                period_fft = 'NAN'
                coherence = 'NAN'

                try:
                    power, f, period, pval, fmax = perform_and_return_lombs(track_sub_no_nan.hours, track_sub_no_nan.detrended)
                    
                    
                except:
                    power, f, period, pval, fmax = ('NAN', 'NAN', 'NAN', 'NAN', 'NAN')

                try: # some tracks had no values need to check this but for now just ignore these.
                    track_len = max(track_sub_no_nan.hours) - min(track_sub_no_nan.hours)
                    master_periods_w.write('\t'.join([str(x) for x in [gene, clone, date, position, channel, interval, trackx, track_len, fmax, period, pval, file_path, filex, period_fft, 'na', coherence]])+'\n')
                
                except:
                    continue

                startline = '\t'.join([str(x) for x in [gene, clone, date, position]])

                for powerx, fx in zip(power, f):
                    master_lomb_traces_w.write(startline + f'\t{powerx}\t{fx}\t{filex}\t{trackx}\tlomb\n')

                for powerx, fx in zip(power_fft, f_fft):
                    master_lomb_traces_w.write(startline + f'\t{powerx}\t{fx}\t{filex}\t{trackx}\tfft\n')

    master_lomb_traces_w.close()
    master_periods_w.close()