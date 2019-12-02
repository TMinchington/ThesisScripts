"""
Detrends classy track output
"""



def detrend_poly_and_savgol(x, y, freedom):

    import numpy as np
    from scipy import signal
    import matplotlib.pyplot as plt
    pfit = np.poly1d(np.polyfit(x, y, freedom)) # fit polynomial to the data
    y_poly_fit = [pfit(i) for i in list(x)]

    y2 = []
    noise = []

    # subtract out the polynomial from the data to remove broad trend

    for yi, yp in zip(y, y_poly_fit):
        y2.append(yi - yp)

    # apply savgol filter to remove noise

    y2s = signal.savgol_filter(y2, 9, 4)

    # subtract savgol filtered data from y2 to get noise

    for svgl, y in zip(y2s, y2):
        noise.append(abs(y - svgl))

    # subtract mean from data

    y2s_mean = np.mean(y2s)
    y2s_sub_mean = [x - y2s_mean for x in y2s]

    fit = y2

    return y2s_sub_mean, fit, noise, y_poly_fit


if __name__ == "__main__":
    
    import argparse
    import pandas as pd
    import matplotlib.pyplot as plt
    import numpy as np

    parser = argparse.ArgumentParser()
    parser.add_argument('adj', help='all_detailed-joinned.csv file from classytrack.py output')
    parser.add_argument('-i', help='interval', type=float)

    args = parser.parse_args()

    df_adj = pd.read_csv(args.adj, sep='\t', header=0)
    df_adj['hours'] = 'gay'
    print(df_adj)

    unique_tracks = set(df_adj.track)
    unique_variables = set(df_adj.variable)
    intense_list = [x for x in unique_variables if  'intensity' in x.lower()]
    df_adj.dropna(inplace=True)
    intensities_frame = df_adj[(df_adj.variable == 'Intensity Mean') & (df_adj.channel == 2)]
    
    del df_adj #remove frame to save memory

    detrended = []
    noise_ls = []
    fit_ls = []
    poly_ls = []
    track2_ls =[]
    time2_ls = []

    print(intensities_frame)

    for trackx in unique_tracks:
        de_sub = intensities_frame[intensities_frame['track'] == trackx]
        de_subx = de_sub.time
        de_suby = de_sub.value

        if len(de_subx) >= 10:
            print(len(de_subx))
            detrended_y, fit, noise, y_poly = detrend_poly_and_savgol(de_subx, de_suby, 3)

            plt.plot(de_subx, de_suby)
            plt.plot(de_subx, detrended_y)
            plt.plot(de_subx, fit)
            plt.plot(de_subx, y_poly)
            plt.show()
            plt.close()

        else:

            detrended_y, fit, noise, y_poly = [[0]*len(de_subx)]*4
        
        print(trackx, len(detrended_y), len(de_subx))

        if len(detrended_y) != len(de_subx):
            exit(trackx)

        time2_ls += list(de_sub.time)
        track2_ls += [trackx]*len(de_subx)
        detrended += detrended_y
        noise_ls += noise
        fit_ls += fit
        poly_ls += y_poly
    
    print('--->', len(intensities_frame), len(detrended))

    intensities_frame['track2'] = track2_ls
    intensities_frame['time2'] = time2_ls
    intensities_frame['detrended'] = detrended
    intensities_frame['fit'] = fit_ls
    intensities_frame['noise'] = noise_ls
    intensities_frame['poly'] = poly_ls
    
    pd.DataFrame.to_csv(intensities_frame, args.adj.replace('.', '-detrended.'), index=None, sep='\t')


    
    
