import multiprocessing as mp
# from multiprocessing import Process as Process
import pandas as pd
# from get_motifs import repressilator_multi

from sys import argv
from resource import getrusage
from resource import RUSAGE_SELF
import gc

import os

def split_load(threads, ls):
    # chr_ls = ['chr-1.txt', 'chr-3.txt', 'chr-6.txt', 'chr-12.txt', 'chr-15.txt', 'chr-18.txt', 'chr-20.txt']
    split_dic = {}

    for x in range(0, threads):

        split_dic[x] = []

    count = 0

    for x in ls:

        split_dic[count].append(x)

        if count == threads-1:

            count = 0

        else:

            count += 1

    return split_dic


def run_multi(key_ls):

    import os

    from get_motifs_quicker import inc_fb_out, read_map_and_fb, amp_fb, dual_fb,\
        write_out_tup_ls, tf_mir_tf, tf1_tf2_tf1, write_out_dic, out_summary

    import os

    for x in key_ls:

        mapdir = x+'/'
        map_file = mapdir+os.path.split(x)[1]+'_network.txt'

        motif_dir = os.path.split(map_file)[0] + '/fast_motifs'

        if not os.path.isdir(motif_dir):
            os.makedirs(motif_dir)

        map_dic, fb_pro, fb_mir = read_map_and_fb(map_file)

        fb_pro_count = write_out_tup_ls(fb_pro, motif_dir + '/auto_regulate.txt')

        fb_mir_count = write_out_tup_ls(fb_mir, motif_dir + '/target_host.txt')

        tf_mir_dic = tf_mir_tf(map_dic)

        tf_mir_counts = write_out_dic(tf_mir_dic, motif_dir + '/tf-mir-tf.txt')

        inc_counts = inc_fb_out(fb_pro, tf_mir_dic, motif_dir + '/inc_fb.txt')

        tf_tf2_dic = tf1_tf2_tf1(map_dic)

        amp_dic = amp_fb(fb_pro, tf_tf2_dic)

        amp_counts = write_out_dic(amp_dic, motif_dir + '/amplified_fb.txt')

        dual_dic = dual_fb(fb_pro, tf_tf2_dic)

        dual_counts = write_out_dic(dual_dic, motif_dir + '/dual_fb.txt')

        print('inc_fb: ', inc_counts['gene'], inc_counts['motif'])
        print('pro_fb: ', fb_pro_count['gene'], fb_pro_count['motif'])
        print('mir_fb: ', fb_mir_count['gene'], fb_mir_count['motif'])
        print('amp_fb: ', amp_counts['gene'], amp_counts['motif'])
        print('dual_fb: ', dual_counts['gene'], dual_counts['motif'])
        print('tf_mir: ', tf_mir_counts['gene'], tf_mir_counts['motif'])

        summary_dic = {'incoherent_fb': inc_counts, 'protein_fb': fb_pro_count, 'targets_host': fb_mir_count,
                       'amplified_feedback': amp_counts, 'dual_feedback': dual_counts, 'tf_mir_loop': tf_mir_counts}

        out_summary(summary_dic, motif_dir + '/motif_summary.txt')



def get_file_ls(tissue_dir):

    import os

    temp_ls = [x for x in os.listdir(tissue_dir) if '.' not in x]
    file_ls = []
    for x in temp_ls:
        print(x)
        if os.path.isfile(tissue_dir+'/'+x+'/'+x+'_network.txt'):

            file_ls.append(tissue_dir+'/'+x)
    # print(file_ls)
    return file_ls


def collect_motifs(file_ls, tiss_dir):

    import os

    motif_dir = tiss_dir+'/motifs'

    if not os.path.isdir(motif_dir):

        os.makedirs(motif_dir)

    first_file = True

    for x in file_ls:
        print(x)
        xfiles = [i for i in os.listdir(x+'/fast_motifs') if '.txt' in i]

        for file in xfiles:

            if first_file:

                file_out = open(motif_dir+'/'+file.replace('.', '_master.'), 'w')

            else:

                file_out = open(motif_dir + '/' + file.replace('.', '_master.'), 'a')


            o_file = open(x+'/fast_motifs/'+file)

            for line in o_file:

                file_out.write(os.path.split(x)[1]+'\t'+line)

        first_file = False


if __name__ == '__main__':

    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("tissue_dir")

    args = parser.parse_args()

    threads = mp.cpu_count()-1

    load_out = split_load(threads, get_file_ls(args.tissue_dir))

    load_out_ls = list(set(list(load_out)))

    print('\n\n\n\n\n\n\n', load_out_ls, '\n\n\n\n\n\n\n')
    # exit()
    '''--------------------------------------------------------------------------------------------------------------'''

    q = None

    jobs = []

    loop_count = 1

    print('lol:', load_out_ls)

    for key in load_out_ls:

        # print('---------------------------------------')
        # print(key)
        key_ls = load_out[key]
        print(key_ls)

        p = mp.Process(target=run_multi, args=(key_ls,))

        jobs.append(p)
        loop_count += 1

    for j in jobs:

        j.start()

    for j in jobs:

        j.join()

    # print(loop_count)\

    collect_motifs(get_file_ls(args.tissue_dir), args.tissue_dir)

exit()
