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
    parser.add_argument('output_location', help='output directory, a folder called fodFromatted will be created in this location')
    args = parser.parse_args()
    
    data_path = pd.read_csv(args.data_loc, header=0)
    track_spots_sub = data_path[(data_path['spot_type']=='track') & (data_path['stat_type']=='spots')]
    
    # print(track_spots_sub.loc[1])

    fod_dir = os.path.join(args.output_location, 'FODformat')

    if not os.path.isdir(fod_dir):
        os.makedirs(fod_dir)

    for index, row in track_spots_sub.iterrows():
        
        (gene, clone, date, position, stat_type, channel, interval, spot_type, root_path, file_path) = row

        gene_path = os.path.join(fod_dir, gene)

        if not os.path.isdir(gene_path):
            os.makedirs(gene_path)

        folder = os.path.join(root_path, file_path)
        detrended_path = os.path.join(folder, 'all_detailed-joined-detrended.tsv')
        detrended_data = pd.read_csv(detrended_path, sep='\t', header=0)

        print(detrended_data.columns)
     
        just_data_i_want = detrended_data[(detrended_data.channel == channel) & (detrended_data.variable == 'Intensity Mean')]

        value_frame = just_data_i_want[['track', 'hours', 'value']]
        detrended_frame = just_data_i_want[['track', 'hours', 'value', 'poly']]
        detrended_frame['detrended']= detrended_frame['value'] - detrended_frame['poly']
        del detrended_frame['value']
        del detrended_frame['poly']
        value_frame_pivot = value_frame.pivot(index='hours', columns='track', values='value')
        detrend_frame_pivot = detrended_frame.pivot(index='hours', columns='track', values='detrended')

        print(value_frame_pivot.head())
        with pd.ExcelWriter(os.path.join(gene_path, f'{gene}_{str(date).replace(".0", "")}_{str(position).replace(".", "-")}_{str(clone).replace(".", "-")}.xlsx'))as writer:  # doctest: +SKIP
            value_frame_pivot.to_excel(writer, sheet_name='Sheet1', header=None, index='hours')
            detrend_frame_pivot.to_excel(writer, sheet_name='Sheet2', header=None, index='hours')
        