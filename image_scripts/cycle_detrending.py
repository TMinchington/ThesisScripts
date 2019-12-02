"""
cycles through statistic files and runs combin outputs and classy track
"""

if __name__ == "__main__":
    
    import argparse
    import os
    import subprocess
    import time
    import pandas as pd

    parser = argparse.ArgumentParser()
    parser.add_argument('data_loc', help='data_locations_file')
    args = parser.parse_args()
    
    data_path = pd.read_csv(args.data_loc, header=0)
    track_spots_sub = data_path[(data_path['stat_type']=='spots') & (data_path['spot_type']=='track')]
    root_list = track_spots_sub.root_path
    folder_list = track_spots_sub.file_path
    channel_list = track_spots_sub.channel
    interval_list = track_spots_sub.interval


    for root, folder_path, channel, interval in zip(root_list, folder_list, channel_list, interval_list):
    
        folder = os.path.join(root, folder_path)
        print(folder)

        joined_file = os.path.join(folder, 'all_detailed-joined.csv')
        # joined_file2 = os.path.join(folder, 'all_detailed-joined_full_track.csv')

        if not os.path.isfile(joined_file):
            subprocess.run(['python', 'combine_outputs.py', folder])
            combined_file = os.path.join(folder, 'all_detailed.csv')
            subprocess.run(['python', 'classy_track.py', combined_file])
        
        # detrended_file = os.path.join(folder, 'all_detailed-joined_full_track-detrended.tsv')

        if not os.path.isfile(joined_file.replace('.csv', '-trim.tsv')):
            print('detrending')
            subprocess.run(['python', 'my_detrending/detrend_my_tracks_trim.py', joined_file, '-c', str(channel), '-i', str(interval)])
            # subprocess.run(['python', 'my_detrending/detrend_my_tracks.py', joined_file2, '-c', str(channel), '-i', str(interval)])