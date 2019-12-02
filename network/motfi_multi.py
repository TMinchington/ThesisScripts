import multiprocessing as mp
# from multiprocessing import Process as Process
import pandas as pd
# from get_motifs import repressilator_multi
from peakME_functions import split_load
from sys import argv
from resource import getrusage
from resource import RUSAGE_SELF
import gc

import os


def motif_stat_multi(outdir, key_ls):


    from get_motifs import mir_mir
    from get_motifs import tf_mir_tf
    from get_motifs import fast_incoherrent_feedback as incoherrent_feedback
    from get_motifs import fast_amp_fb as amplified_feedback
    from get_motifs import dual_amplified_feedback
    from get_motifs import interaction_types_low_mem

    file_ls = []

    for x in key_ls:

        print(x)
        # exit()
        frame_dir = '{}/ran_map-{}'.format(outdir, x)
        file_path = '{}/ran_map-{}.txt'.format(frame_dir, x)

        file_ls.append(file_path)

    print('Made a list of files:\n')

    for file in file_ls:

        print(file)

    for file in file_ls:

        file_dir = os.path.split(file)[0]

        motif_dir = file_dir+'/motif'
        stat_dir = file_dir+'/stat'

        if not os.path.isdir(motif_dir):

            os.makedirs(motif_dir)

        if not os.path.isdir(stat_dir):

            os.makedirs(stat_dir)

        xmap = pd.DataFrame(pd.read_csv(file, sep='\t', header=0, dtype={'score': str, 'distance_abs': str,
                                                                      'distance_act': str, 'num_sites': str}))

        mir_mir(xmap, motif_dir)
        gc.collect()

        tf_mir_tf(xmap, motif_dir)

        incoherrent_feedback(xmap, motif_dir)

        fb_file = '{}/genes_fb_mir_new.txt'.format(motif_dir)

        amplified_feedback(fb_file, xmap, motif_dir)

        amp_file = '{}/amp_fb_new.txt'.format(motif_dir)

        dual_amplified_feedback(amp_file, fb_file, motif_dir)

        gc.collect()

        interaction_types_low_mem(xmap, motif_dir)



if __name__ == '__main__':

    threads = 4

    outdir = argv[1]
    num_net = int(argv[2])


    load_out = split_load(threads, range(0, num_net))

    load_out_ls = list(set(list(load_out)))

    print('\n\n\n\n\n\n\n', load_out_ls, '\n\n\n\n\n\n\n')
    # exit()
    '''--------------------------------------------------------------------------------------------------------------'''

    q = None

    jobs = []

    loop_count = 1

    print(load_out_ls)

    for key in load_out_ls:

        # print('---------------------------------------')
        # print(key)
        key_ls = load_out[key]
        # print(key_ls)

        p = mp.Process(target=motif_stat_multi, args=(outdir, key_ls))

        jobs.append(p)
        loop_count += 1

    for j in jobs:

        j.start()

    for j in jobs:

        j.join()

    # print(loop_count)\

exit()
