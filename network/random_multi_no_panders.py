import multiprocessing as mp
# from multiprocessing import Process as Process
# import pandas as pd
from peakME_functions import split_load
from sys import argv
# from Random_net import multi_random
from random import shuffle
import os
import gc

def multi_random(dir, map_dic, in_ls):

    for x in in_ls:

        print(x)

        shuffle(map_dic['pro_targ'])

        shuffle(map_dic['mir_tar'])

        frame_dir = '{}/ran_map-{}'.format(dir, x)

        if not os.path.isdir(frame_dir):

            os.makedirs(frame_dir)

        file_path = '{}/ran_map-{}.txt'.format(frame_dir, x)

        outfile = open(file_path, 'w')

        outfile.write(header_line)

        for x in range(0, len(map_dic['pro_targ'])):

            outfile.write(map_dic['pro_reg'][x])
            outfile.write('\t')
            outfile.write(map_dic['pro_targ'][x])
            outfile.write('\n')

        for x in range(0, len(map_dic['mir_tar'])):

            outfile.write(map_dic['mir_reg'][x])
            outfile.write('\t')
            outfile.write(map_dic['mir_tar'][x])
            outfile.write('\n')

        outfile.close()


# pro_frame = pd.DataFrame(pd.read_csv(argv[3], sep='\t', header=0))
# mir_frame = pd.DataFrame(pd.read_csv(argv[4], sep='\t', header=0))

pro_file = open(argv[3])
mir_file = open(argv[4])

map_dic = {}

map_dic['pro_reg'] = []
map_dic['pro_targ'] = []

map_dic['mir_reg'] = []
map_dic['mir_tar'] = []

line_count = 0

for line in pro_file:

    if line_count == 0:

        header_line = line
        line_count += 1

        continue

    line = line.strip()
    line = line.split('\t')

    # print(line[:3], line[3:])

    map_dic['pro_reg'].append('\t'.join(line[:3]))
    map_dic['pro_targ'].append('\t'.join(line[3:]))


line_count = 0

for line in mir_file:

    if line_count == 0:

        line_count += 1

        continue

    line = line.strip()
    line = line.split('\t')

    map_dic['mir_reg'].append('\t'.join(line[:3]))
    map_dic['mir_tar'].append('\t'.join(line[3:]))



if __name__ == '__main__':

    threads = 1

    xdir = argv[1]
    num_net = int(argv[2])
    load_out = split_load(threads, range(0, num_net))

    load_out_ls = list(set(list(load_out)))

    print('\n\n\n\n\n\n\n', load_out_ls, '\n\n\n\n\n\n\n')

    load_check_ls = []

    for x in load_out_ls:

        print(len(load_out[x]))

        load_check_ls.append(len(load_out[x]))



    '''--------------------------------------------------------------------------------------------------------------'''

    q = None

    jobs = []

    loop_count = 1


    for key in load_out_ls:

        # print(key)

        key_ls = load_out[key]

        p = mp.Process(target=multi_random, args=(xdir, map_dic, key_ls))

        jobs.append(p)
        loop_count += 1

    for j in jobs:

        j.start()

    for j in jobs:

        j.join()

    print(loop_count)


gc.collect()
exit()