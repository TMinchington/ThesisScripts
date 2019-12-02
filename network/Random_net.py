# for randomising the network
def random_net():

    import pandas as pd
    from random import shuffle
    from sys import argv
    import os
    import subprocess

    num_net = 1  # Number of networks to generate

    split_dir = argv[1].replace('.tsv', '-split')

    if not os.path.isdir(split_dir):
        os.makedirs(split_dir)

    pro_file = '{}/pro_frame.txt'.format(split_dir)
    mir_file = '{}/mir_frame.txt'.format(split_dir)

    def split_maps():

        net_frame = pd.read_csv(argv[1], sep='\t', header=0, dtype={'score': str, 'distance_abs': str,
                                                                    'distance_act': str, 'num_sites': str})

        del net_frame['score']
        del net_frame['distance_act']
        del net_frame['distance_abs']
        del net_frame['num_sites']

        print(net_frame.head())

        pro_frame = net_frame.loc[net_frame['reg_type'] == 'protein_coding']
        mir_frame = net_frame.loc[net_frame['reg_type'] != 'protein_coding']

        net_frame = None

        pd.DataFrame.to_csv(pro_frame, pro_file, sep='\t', index=False)
        pd.DataFrame.to_csv(mir_frame, mir_file, sep='\t', index=False)

        pro_frame = None
        mir_frame = None

    dir = argv[2]


    def multi_random(dir, pro_frame, mir_frame):

        file_ls = []

        for x in range(0, num_net):

            pro_reg = pro_frame[['regulator', 'regulator_name', 'reg_type']]
            pro_targ = pro_frame[['target', 'target_name', 'target_type']]

            index_ls = list(pro_targ.index)

            shuffle(index_ls)

            pro_targ.index = index_ls

            pro_frame = pd.DataFrame(pd.concat([pro_reg, pro_targ], axis=1))

            print(pro_frame)

            mir_reg = mir_frame[['regulator', 'regulator_name', 'reg_type']]
            mir_targ = mir_frame[['target', 'target_name', 'target_type']]

            index_ls = list(mir_targ.index)

            shuffle(index_ls)

            mir_targ.index = index_ls

            mir_frame = pd.DataFrame(pd.concat([mir_reg, mir_targ], axis=1))

            frame_dir = '{}/ran_map-{}'.format(dir, x)

            if not os.path.isdir(frame_dir):
                os.makedirs(frame_dir)

            file_path = '{}/ran_map-{}.txt'.format(frame_dir, x)

            pd.DataFrame.to_csv(pd.DataFrame(pd.concat([pro_frame, mir_frame], axis=0)), file_path, index=False, sep='\t')

            file_ls.append(file_path)


    def make_randoms():

        split_maps()
        subprocess.run(["python", "random_multi_no_panders.py", dir, str(num_net), pro_file, mir_file], check=True)

    def run_motifs():

        subprocess.run(["python", "motfi_multi.py", dir, str(num_net)], check=True)

    def collect_random_maps():

        subprocess.run(["python", "collect_random.py", dir, dir], check=True)



    # make_randoms()
    run_motifs()
    # collect_random_maps()


random_net()

#
# # bring all data together
#
# all_motif_dir = '{}/all_random_motifs'.format(dir)
#
# if not os.path.isdir(all_motif_dir):
#
#     os.makedirs(all_motif_dir)
#
#
# all_reg_out = open('{}/random_all_reg_count.txt'.format(all_motif_dir), 'w')
# all_target_regulator_count = open('{}/random_all_targ_reg_count.txt'.format(all_motif_dir), 'w')
# all_amp_fb_count = open('{}/random_all_fb_count.txt', 'w')
#
