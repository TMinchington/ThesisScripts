"""
This file cycles though the output files and joins them into one file for processing in classyTrack.py
"""

def cycle_files(folder_path, outfile):

    from os import listdir

    file_ls = listdir(folder_path)
    file_ls = [x for x in file_ls if '.csv' in x and 'all_' not in x]

    o_out  = open(outfile, 'w')
    o_out.write('\nDetailed\n ==================== \nVariable,Value,Unit,Category,Channel,Collection,Time,TrackID,ID,\n')
    
    for file in file_ls:
        # print(file)
        try:
            with open(folder_path + '/' + file) as openFile:
                in_data = False
                head_line = False
                position_file = False

                for line in openFile:
                    split_line = line.strip().split(',')
                    
                    if line.startswith(' ='):
                        in_data = True
                        head_line = True

                    elif in_data and head_line:
                        head_line = False
                        print(split_line)
                    
                        if line.startswith('Position'):
                            position_file = True
                            pos_xn, pos_yn, pos_zn = split_line[:3]

                        elif len(split_line) == 9:
                            variable_name = split_line[0]

                        else:
                            print('breaking: ', file)
                            break

                        # print()

                    elif in_data and position_file:
                        # print(split_line)
                        # print(split_line)
                        pos_x, pos_y, pos_z, unit, category, collection, time, trackID, spot_id, other = split_line

                        out_strX = ','.join([pos_xn, pos_x, unit, category, '', collection, time, trackID, spot_id, other]) + '\n'
                        out_strY = ','.join([pos_yn, pos_y, unit, category, '', collection, time, trackID, spot_id, other]) + '\n'
                        out_strZ = ','.join([pos_zn, pos_z, unit, category, '', collection, time, trackID, spot_id, other]) + '\n'

                        o_out.write(out_strX)
                        o_out.write(out_strY)
                        o_out.write(out_strZ)

                    elif in_data and not position_file:
                        # print(split_line)
                        variable_value, unit, category,  channel, image, time, trackID, spot_id, other = split_line

                        out_str = ','.join([variable_name, variable_value,
                                            unit, category,  channel, image, time, trackID, spot_id, other]) + '\n'

                        # print(out_str)

                        o_out.write(out_str)

                    else:

                        continue
        except:
            continue
    o_out.close()

if __name__ == "__main__":

    import argparse
    import os
    parser = argparse.ArgumentParser()
    parser.add_argument('folder_path')
    args = parser.parse_args()
    

    folder_ls = [x for x in os.listdir(args.folder_path) if '.' not in x]
    cycle_files(args.folder_path, args.folder_path + '/all_detailed.csv')
#    for folder in folder_ls:
#        print(folder)
#        cycle_files(args.folder_path + '/' + folder, args.folder_path + '/' + folder+ '/all_detailed.csv')
