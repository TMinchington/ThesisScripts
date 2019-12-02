from sys import argv
import pandas as pd
from time import time


#
# print(argv[1])
# exit()


# print(map.columns)


def incoherrent_feedback(map, outdir):

    import pandas as pd

    outfile2 = open('{}/genes_fb_mir.txt'.format(outdir), 'w')
    hit_ls = []

    map = pd.DataFrame(map)
    map.drop_duplicates(inplace=True)
    # print(map.columns)
    map_len = len(map)
    in_both = map.loc[map['regulator'].isin(list(set(list(map['target']))))]

    # print(in_both.loc[in_both['reg_type'] == 'miRNA'])
    # print(map.loc[map['reg_type'] == 'miRNA'])

    # print('\n\n\n\n\n\n\n\n')

    protein_sub = in_both.loc[(in_both['target_type'] == 'protein_coding') & (in_both['reg_type'] == 'protein_coding')]

    # print(protein_sub)

    ls_1 = list(protein_sub['target'])
    ls_2 = list(protein_sub['regulator'])

    feedback_ls = []

    for x in range(0, len(ls_1)):

        # print(ls_1[x], ls_2[x])

        if ls_1[x] == ls_2[x]:
            # print(ls_1[x])
            feedback_ls.append(ls_1[x])
    # print(len(feedback_ls))
    feedback_ls = list(set(feedback_ls))
    # print(len(feedback_ls))

    for target in feedback_ls:

        reg_sub = map.loc[map['regulator'] == target]
        reg_mir_sub = reg_sub.loc[reg_sub['target_type'] == 'miRNA']

        target_name = list(reg_sub['regulator_name'])[0]
        reg_mir_ls = list(set(list(reg_mir_sub['target_name'])))

        reg_sub2 = map.loc[(map['regulator_name'].isin(reg_mir_ls)) & (map['target'] == target)]

        # print(reg_sub2)


        match_mir_ls = list(set(list(reg_sub2['regulator_name'])))



        outfile2.write('{}\t{}\t{}\n'.format(target_name, target, len(match_mir_ls),' '.join(match_mir_ls)))


    outfile2.close()

    # exit()


def fast_incoherrent_feedback(map, outdir):

    import numpy as np

    print('running incoherrent feedback')

    outfile2 = open('{}/genes_fb_mir_new.txt'.format(outdir), 'w')

    map.drop_duplicates(inplace=True, subset=['regulator_name', 'target_name'])

    protein_sub = map.loc[(map['target_type'] == 'protein_coding') & (map['reg_type'] == 'protein_coding')]

    protein_sub = pd.DataFrame(protein_sub)

    protein_sub['self_match'] = protein_sub['regulator'] == protein_sub['target']
    # protein_sub['self_match'] = np.where(protein_sub['regulator'] == protein_sub['target'], True, False)
    # print(len(protein_sub))
    self_reg = pd.DataFrame(protein_sub.loc[protein_sub['self_match'] == True])

    # print(len(self_reg))

    reg_name = list(self_reg['regulator_name'])
    reg_code = list(self_reg['regulator'])

    mir_reg = map.loc[(map['target_type'] == 'protein_coding') & (map['reg_type'] == 'miRNA')]
    mir_tar = map.loc[(map['target_type'] == 'miRNA') & (map['reg_type'] == 'protein_coding')]


    mir_bind = pd.DataFrame(pd.concat([mir_reg, mir_tar], axis=0))

    # print(mir_bind)

    for x in range(0, len(reg_code)):

        reg = reg_code[x]
        nam = reg_name[x]

        # print('\n\n----------------------{}-------------------------\n'.format(nam))

        reg_sub = mir_bind.loc[(mir_bind['target_name'] == nam) | (mir_bind['regulator_name'] == nam)]

        # print(reg_sub)

        no_reg_sub = reg_sub.loc[reg_sub['target_name'] != nam]

        no_reg_sub_ls = list(no_reg_sub['target_name'])

        # print(no_reg_sub_ls)

        reg_sub = reg_sub.loc[reg_sub['regulator_name'].isin(no_reg_sub_ls)]

        # reg_sub.drop_duplicates(inplace=True, subset=['regulator_name', 'target_name'])

        # print('\n\n----------------------{}-------------------------\n'.format(nam))
        # print(reg_sub)

        # reg_sub = reg_sub.loc[reg_sub['target_name'] != nam]
        # reg_sub2 = reg_sub.loc[reg_sub['regulator_name'] != nam]


        # test_ls1 = list(set(list(reg_sub['regulator_name'])))
        # test_ls2 = list(set(list(reg_sub2['target_name'])))

        # print(test_ls1)
        # print(test_ls2)

        # for xi in test_ls1:
        #
        #     if xi not in test_ls2:
        #
        #         print('ERROR!!!!')
        #         print(xi, nam)
        #         print('\n\n')


        reg_ls = list(set(list(reg_sub['regulator_name'])))

        reg_ls2 = [x for x in reg_ls if x.startswith('hsa')]

        outfile2.write('{}\t{}\t{}\t{}\t{}\n'.format(nam, reg, len(reg_ls), len(reg_ls2), ' '.join(reg_ls)))



'''-----------------------------------------------------------------------------------------------------------------'''


def mir_mir(xmap, outdir):

    print('running mir mir')

    outfile = open('{}/genes_mir_self.txt'.format(outdir), 'w')


    mir_sub = xmap.loc[(xmap['reg_type'] == 'miRNA') & (xmap['target_type'] == 'miRNA')]

    mir_self = pd.DataFrame(mir_sub.loc[mir_sub['regulator'] == mir_sub['target']])
    mir_self.drop_duplicates(inplace=True)
    # print(mir_self)

    mir_ls = list(set(list(mir_self['regulator_name'])))

    for mir in mir_ls:

        outfile.write('{}\n'.format(mir))

    outfile.close()

# mir_mir(pd.read_csv(argv[1], sep='\t', header=0), argv[2])


'''-----------------------------------------------------------------------------------------------------------------'''


def tf_mir_tf(mapf, outdir):

    print('running tf mir tf')

    outfile = open('{}/tf_mir_tf.txt'.format(outdir), 'w')

    # print(mapf.columns)

    protein_sub = mapf.loc[(mapf['reg_type'] != 'miRNA')]

    regulator_ls = list(set(list(protein_sub['regulator_name'])))

    # print(regulator_ls)
    # print(len(regulator_ls))

    tf_dic = {}

    for reg in regulator_ls:

        reg_sub = mapf.loc[(mapf['regulator_name'] == reg) & (mapf['target_type'] == 'miRNA')]

        mir_ls = list(set(reg_sub['target_name']))

        # print(mir_ls)
        mapf_reg = mapf.loc[mapf['target_name'] == reg]

        tf_dic[reg] = []

        for mir in mir_ls:

            mir_sub = mapf_reg.loc[(mapf_reg['regulator_name'] == mir)]

            if reg in list(mir_sub['target_name']):

                tf_dic[reg].append(mir)


    tf_keys = list(tf_dic)

    for key in tf_keys:

        # print(key, tf_dic[key])
        if len(tf_dic[key]) == 0:

            continue

        outfile.write('{}\t{}\n'.format(key, ' '.join(tf_dic[key])))

    outfile.close()


'''-----------------------------------------------------------------------------------------------------------------'''

def amplified_feedback(feedback_file, map, outdir):

    print('\n running amplified feedback')
    feedback_ls = []

    outfile = open('{}/amp_fb.txt'.format(outdir), 'w')

    fb_file = open(feedback_file)

    for line in fb_file:

        line = line.strip()
        split_line = line.split()

        feedback_ls.append(split_line[0])

    fb_file.close()
    # print(len(map))
    # print(len(feedback_ls))
    feedback_ls = list(set(feedback_ls))
    # print(len(feedback_ls))

    fb_sub = map.loc[(map['target_name'].isin(feedback_ls)) & (map['reg_type'] == 'protein_coding')] # creates frame where targets are already fb and targets

    # print(fb_sub)

    amp_ls = []

    for tf in feedback_ls:

        # print(tf)

        tf_sub = fb_sub.loc[fb_sub['target_name'] == tf]

        reg_ls = list(set(list(tf_sub['regulator_name'])))

        for reg in reg_ls:

            reg_sub = map.loc[(map['target_name'] == reg)]

            if tf in list(set(list(reg_sub['regulator_name']))):

                # print(tf, reg)

                if tf == reg or '{}{}'.format(tf, reg) in amp_ls or '{}{}'.format(reg, tf) in amp_ls:

                    continue

                amp_ls.append('{}{}'.format(tf, reg))

                outfile.write('{}\t{}\n'.format(tf, reg))


    outfile.close()


def fast_amp_fb(feedback_file, map, outdir):

    print('\n running amplified feedback faster')
    feedback_ls = []

    outfile = open('{}/amp_fb_new.txt'.format(outdir), 'w')

    fb_file = open(feedback_file)

    for line in fb_file:
        line = line.strip()
        split_line = line.split()

        feedback_ls.append(split_line[0])

    fb_file.close()
    # print(len(map))
    # print(len(feedback_ls))
    feedback_ls = list(set(feedback_ls))

    tf_sub = map.loc[(map['target_type'] == 'protein_coding') & (map['reg_type'] == 'protein_coding')]

    tf_ls = list(set(list(tf_sub['regulator_name'])))

    tf_sub = tf_sub.loc[tf_sub['target_name'].isin(tf_ls)]

    # print(tf_sub)

    for tf in feedback_ls:

        tf_sub2 = tf_sub.loc[tf_sub['target_name'] == tf]

        # print(tf_sub2)

        tf_sub3 = tf_sub.loc[tf_sub['regulator_name'] == tf]

        # print(tf_sub3)

        tf_sub4 = tf_sub3.loc[tf_sub3['target_name'].isin(list(set(list(tf_sub2['regulator_name']))))]

        # print(tf_sub4)

        amp_ls = [x for x in list(set(list(tf_sub4['target_name']))) if not x == tf]

        outfile.write('{}\t{}\t{}\n'.format(tf, len(amp_ls), ' '.join(amp_ls)))




'''-----------------------------------------------------------------------------------------------------------------'''

# def dual_amplified_feedback(amp_feedback_file, feedback_file, outdir):
#
#     import pandas as pd
#
#     print('\nrunning dual feedback')
#
#     # print('\n running amplified feedback')
#     feedback_ls = []
#
#     fb_file = open(feedback_file)
#
#     for line in fb_file:
#         line = line.strip()
#         split_line = line.split()
#
#         feedback_ls.append(split_line[0])
#
#     fb_file.close()
#     # print(len(map))
#     # print(len(feedback_ls))
#     feedback_ls = list(set(feedback_ls))
#     # print(len(feedback_ls))
#     #
#     amp_df = pd.DataFrame(pd.read_csv(amp_feedback_file, sep='\t', header=None))
#
#     d_amp_df = amp_df.loc[amp_df[1].isin(feedback_ls)]
#
#     pd.DataFrame.to_csv(d_amp_df, '{}/dual_amp_fb.txt'.format(outdir), sep='\t', header=None, index=False)
#
#     del amp_df
#     del d_amp_df

'''-----------------------------------------------------------------------------------------------------------------'''

def dual_amplified_feedback(amp_feedback_file, feedback_file, outdir):

    print('running dual amp')

    feedback_ls = []

    fb_file = open(feedback_file)

    for line in fb_file:
        line = line.strip()
        split_line = line.split()

        feedback_ls.append(split_line[0])

    fb_file.close()

    feedback_ls = list(set(feedback_ls))

    amp_file = open(amp_feedback_file)

    daff = open('{}/dual_amp_fb.txt'.format(outdir), 'w')
    damp_ls=[]


    for line in amp_file:

        line = line.strip()
        line = line.split('\t')

        daff.write(line[0])
        daff.write('\t')

        try:

            damp_ls = line[2].split(' ')

        except IndexError:

            daff.write('0\tNone\n')

            continue

        if len(damp_ls) == 0:

            daff.write('0\tNone\n')

            continue

        damp_ls = [x for x in damp_ls if x in feedback_ls]

        if len(damp_ls) == 0:

            daff.write('0\tNone\n')

            continue

        daff.write('{}\t{}\n'.format(len(damp_ls), ' '.join(damp_ls)))

    del feedback_ls
    del damp_ls



'''-----------------------------------------------------------------------------------------------------------------'''

def repressilator(map):

    print('running repressilator')

    outfile = open('F:/PhD - Nancy/MAP/MOTIFS/repressialtor.txt', 'w')

    map = pd.DataFrame(map)

    protein = map.loc[(map['reg_type'] == 'protein_coding') & (map['target_type'] == 'protein_coding')]

    tf_list = list(set(list(protein['regulator_name'])))
    # count=0
    for x in tf_list:

        x_frame = protein.loc[protein['regulator_name'] == x]

        y_list = list(set(x_frame['target_name']))

        for y in y_list:

            y_frame = protein.loc[protein['regulator_name'] == y]

            z_list = list(set(y_frame['target_name']))

            for z in z_list:

                z_frame = protein.loc[protein['regulator_name'] == z]

                zx_frame = z_frame.loc[z_frame['target_name'] == x]

                # count += 1
                # print(count)

                if len(zx_frame):

                    # print(x, y, z)

                    outfile.write('{}\t{}\t{}\n'.format(x, y, z))


def repressilator_multi(protein, tf_list, key, outdir):

    outfile = open('{}/repressilator_files/repressialtor_{}.txt'.format(outdir, key), 'w')

    for x in tf_list:

        x_frame = protein.loc[protein['regulator_name'] == x]

        y_list = list(set(x_frame['target_name']))

        for y in y_list:

            y_frame = protein.loc[protein['regulator_name'] == y]

            z_list = list(set(y_frame['target_name']))

            for z in z_list:

                z_frame = protein.loc[protein['regulator_name'] == z]

                zx_frame = z_frame.loc[z_frame['target_name'] == x]

                # count += 1
                # print(count)

                if len(zx_frame) > 0:

                    if x == y or x == z or z == y:

                        continue

                    # print(x, y, z)

                    outfile.write('{}\t{}\t{}\n'.format(x, y, z))


def mir_regulators(map, outdir):

    print('running mir regulators')

    mir_sub = map.loc[map['reg_type'] == 'miRNA']

    pro_sub = map.loc[map['reg_type'] == 'protein']

    pro_ls = list(set(list(pro_sub['regulator_name'])))

    pro_data = pd.DataFrame(mir_sub['regulator_name'].value_counts())
    print(pro_data)
    pd.DataFrame.to_csv(pro_data, '{}/mir_reg_TF.txt'.format(outdir))



def interaction_types(xmap2, outdir):


    print('running interaction types')

    suber = xmap2.loc[xmap2['reg_type'] == 'miRNA']
    mir_pro = len(suber.loc[suber['target_type'] == 'protein_coding'])

    suber = xmap2.loc[xmap2['reg_type'] == 'protein_coding']
    pro_mir = len(suber.loc[suber['target_type'] == 'miRNA'])

    suber = xmap2.loc[xmap2['reg_type'] == 'miRNA']
    mir_mir = len(suber.loc[suber['target_type'] == 'miRNA'])

    suber = xmap2.loc[xmap2['reg_type'] == 'protein_coding']
    pro_pro = len(suber.loc[suber['target_type'] == 'protein_coding'])

    tf_ls = list(set(list(suber['regulator_name'])))

    pro_tf = len(suber.loc[suber['target_name'].isin(tf_ls)])

    suber = xmap2.loc[xmap2['reg_type'] == 'miRNA']
    mir_tf = len(suber.loc[suber['target_name'].isin(tf_ls)])

    outfile = open('{}/simple_motifs.txt'.format(outdir), 'w')

    outfile.write('mir_pro\t{}\n'.format(mir_pro))
    outfile.write('pro_mir\t{}\n'.format(pro_mir))
    outfile.write('pro_pro\t{}\n'.format(pro_pro))
    outfile.write('mir_mir\t{}\n'.format(mir_mir))
    outfile.write('pro_tf\t{}\n'.format(pro_tf))
    outfile.write('mir_tf\t{}\n'.format(mir_tf))


def interaction_types_low_mem(xmap, outdir):

    print('running interaction types ( low memory version )')

    out_dic = {}

    reg_ls = list(xmap['reg_type'])
    targ_ls = list(xmap['target_type'])

    for x in range(0, len(reg_ls)):

        try:

            out_dic[reg_ls[x] + '-' + targ_ls[x]] += 1

        except KeyError:

            out_dic[reg_ls[x] + '-' + targ_ls[x]] = 1

    del reg_ls
    del targ_ls

    outfile = open('{}/simple_motifs.txt'.format(outdir), 'w')

    for x in list(out_dic):

        outfile.write('{}\t{}\n'.format(x, out_dic[x]))





# functions to run
def run_when_single():
    map = pd.DataFrame(pd.read_csv(argv[1], sep='\t', header=0, dtype={'score': str, 'distance_abs': str,
                                                                      'distance_act': str, 'num_sites': str}))
    # print('\n\n----------------------\n')
    # map.drop_duplicates(inplace=True, subset=['regulator_name', 'target_name'])
    # map = pd.DataFrame(map)
    print(map.head())
    outdir = argv[2]
    #
    mir_regulators(map, outdir)
    interaction_types(map, outdir)
    # exit()
    #
    # times_ls = []
    fast_incoherrent_feedback(map, argv[2])
    fb_file = '{}/genes_fb_mir_new.txt'.format(outdir)
    #
    #
    # t0 = time()
    mir_mir(map, outdir)
    # t1 = time()
    #
    # times_ls.append(''.join(['mir-mir: ', str(t1-t0)]))
    #
    #
    # t0 = time()

    # t1 = time()
    #
    # times_ls.append(''.join(['Fast incoherrent: ', str(t1-t0)]))

    #
    # t0 = time()
    tf_mir_tf(map, outdir)
    # t1 = time()
    #
    # times_ls.append(''.join(['tf_mir_tf: ', str(t1-t0)]))
    #
    # t0 = time()
    # incoherrent_feedback(map, outdir)
    # t1 = time()
    #
    # times_ls.append(''.join(['incoherrent FB: ', str(t1-t0)]))
    #
    # t0 = time()
    # amplified_feedback(fb_file, map, outdir)
    # t1 = time()
    #
    # times_ls.append(''.join(['amp_fb: ', str(t1-t0)]))
    #
    # t0 = time()
    fast_amp_fb(fb_file, map, outdir)
    # t1 = time()
    #
    # times_ls.append(''.join(['fast_amp_fb: ', str(t1-t0)]))
    #
    amp_file = '{}/amp_fb_new.txt'.format(outdir)
    #
    # t0 = time()
    dual_amplified_feedback(amp_file, fb_file, outdir)
    # t1 = time()
    #
    # times_ls.append(''.join(['dual amp fb: ', str(t1-t0)]))
    # repressilator_multi(map)
    #
    # for x in times_ls:
    #
    #     print(x)
if __name__ == '__main__':
    run_when_single()