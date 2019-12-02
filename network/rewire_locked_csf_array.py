# rewire the network rather than randomise by joining

def load_dic(network):

    dic_pro = {}
    dic_pro_auto = {}
    dic_mir = {}

    with open(network) as o_net:

        first_line = True

        for line in o_net:

            if first_line:

                first_line = False

                continue

            split_line = line.strip().split('\t')

            if split_line[2] == "protein_coding":

                out_node = '\t'.join(split_line[0:3])
                in_node = '\t'.join(split_line[3:6])

                if out_node != in_node:

                    dic_pro['\t'.join([out_node, in_node])] = (out_node, in_node)

                else:

                    dic_pro_auto['\t'.join([out_node, in_node])] = (out_node, in_node)

            else:

                out_node = '\t'.join(split_line[0:3])
                in_node = '\t'.join(split_line[3:6])

                dic_mir['\t'.join([out_node, in_node])] = (out_node, in_node)

    return dic_pro, dic_mir, dic_pro_auto


def shuffle_node(net_dic, ran_key1, ran_key2):

    if ran_key1 == ran_key2:

        return net_dic, False
    net_ls = list(net_dic)
    rank1 = net_ls[ran_key1]
    rank2 = net_ls[ran_key2]
    # print('---------------')
    # print('rk1:', rank1)
    # print('rk2:', rank2)
    # print('---------------')

    edge1 = net_dic[rank1]
    edge2 = net_dic[rank2]

    if edge1[1] == edge2[1]:

        return net_dic, False

    # print('edge1:', edge1)
    # print('edge2:', edge2)
    # print('---------------')

    del net_dic[rank1]
    del net_dic[rank2]

    new_edge1 = (edge1[0], edge2[1])
    new_edge2 = (edge2[0], edge1[1])

    # print('new edge1:', new_edge1)

    # print('new edge2:', new_edge2)
    # print('---------------')

    new_edge1_key = '\t'.join([new_edge1[0], new_edge1[1]])
    new_edge2_key = '\t'.join([new_edge2[0], new_edge2[1]])

    if new_edge1_key in net_dic or new_edge2_key in net_dic or new_edge1[0] == new_edge1[1] or new_edge2[0] == new_edge2[1]:

        net_dic[rank1] = edge1
        net_dic[rank2] = edge2

        return net_dic, False

    else:

        net_dic[new_edge1_key] = new_edge1
        net_dic[new_edge2_key] = new_edge2

        return net_dic, True


def numpy_random_ls(loops, size):

    import numpy as np

    np_ls = np.random.RandomState().randint(0, size, loops)

    return np_ls


def run_job(net_path, x_ls, net_dic_pro1, net_dic_mir1):

    made_new_pro = 0
    kept_old_pro = 0
    made_new_mir = 0
    kept_old_mir = 0

    loops = 5000000

    for x in x_ls:

        t3 = time.time()

        net_dic_pro = net_dic_pro1.copy()
        net_dic_mir = net_dic_mir1.copy()

        if not os.path.isdir('{}/rewire_locked_array/ran_map-{}'.format(net_path, x)):
            os.makedirs('{}/rewire_locked_array/ran_map-{}'.format(net_path, x))

        outfile = open('{}/rewire_locked_array/ran_map-{}/ran_map-{}.txt'.format(net_path, x, x), 'w')
        outfile.write('regulator\tregulator_name\treg_type\ttarget\ttarget_name	target_type\n')

        net_pro_len = len(net_dic_pro)-1
        net_mir_len = len(net_dic_mir)-1
        ran_ls_1p = numpy_random_ls(loops, net_pro_len)
        ran_ls_2p = numpy_random_ls(loops, net_pro_len)

        ran_ls_1m = numpy_random_ls(loops, net_mir_len)
        ran_ls_2m = numpy_random_ls(loops, net_mir_len)

        # print(ran_ls_1p[0:20])

        target_edges_pro = 1.1*net_pro_len
        target_edges_mir = 1.1*net_mir_len

        print('edges to hit pro: ', target_edges_pro)
        print('edges to hit mir: ', target_edges_mir)

        for x in range(0, loops):

            # print(made_new_pro/target_edges_pro*100)
            # print(made_new_mir/target_edges_mir*100)

            net_dic, new_edge = shuffle_node(net_dic_pro, ran_ls_1p[x], ran_ls_2p[x])

            if new_edge:

                made_new_pro += 1

                if target_edges_mir < made_new_mir and target_edges_pro < made_new_pro:

                    print('edge_break!', x)
                    break

            else:

                kept_old_pro += 1

            if target_edges_mir < made_new_mir:

                continue

            net_dic, new_edge = shuffle_node(net_dic_mir, ran_ls_1m[x], ran_ls_2m[x])

            if new_edge:

                made_new_mir += 1

            else:

                kept_old_mir += 1

            # new_pro_ls.append(made_new_pro)
            # new_mir_ls.append(made_new_mir)

        # print(made_new_pro, kept_old_pro)
        # print(made_new_mir, kept_old_mir)
        #
        # print('pro_over_edges', made_new_pro / len(net_dic_pro) * 100)
        # print('pro_over_edges', made_new_mir / len(net_dic_mir) * 100)

        for x in net_dic_auto:

            outfile.write(x + '\n')

        for x in net_dic_pro:
            outfile.write(x + '\n')

        for x in net_dic_mir:
            outfile.write(x + '\n')

        made_new_pro = 0
        kept_old_pro = 0
        made_new_mir = 0
        kept_old_mir = 0

    print('** run job', time.time() - t3)

if __name__ == "__main__":

    import argparse
    # import matplotlib.pyplot as plt
    import multiprocessing as mp
    import os
    import time

    # t1 = time.time()

    parser = argparse.ArgumentParser()

    parser.add_argument("network")
    # parser.add_argument("strt", type=int)
    # parser.add_argument("stp", type=int)
    # parser.add_argument("cores", type=int)
    parser.add_argument("array", type=int)

    args = parser.parse_args()

    net_dic_pro1, net_dic_mir1, net_dic_auto = load_dic(args.network)

    # print('** load net', time.time()-t1)
    # t2 = time.time()
    # new_pro_ls = []
    # new_mir_ls = []

    net_path = os.path.split(args.network)[0]

    if not os.path.isdir(net_path+'/rewire_locked_array'):

        os.mkdir(net_path+'/rewire_locked_array')

    run_job(net_path, [args.array-1], net_dic_pro1, net_dic_mir1)

    # list1000 = list(range(args.strt, args.stp))

    # print(list1000)

    # lists = {}

    # pos_count = 0
    # print('** cycle folders', time.time() - t2)

    # for x in list1000:
    #
    #     # print(pos_count)
    #
    #     try:
    #
    #         lists[pos_count].append(x)
    #
    #     except KeyError:
    #
    #         lists[pos_count] = [x]
    #
    #     pos_count += 1
    #
    #     if pos_count == args.cores:
    #         pos_count = 0

    # print(lists)

    # jobs = []

    # for x in lists:
    #     jobs.append(mp.Process(target=run_job,
    #                            args=[net_path, lists[x], net_dic_pro1, net_dic_mir1]))
    #
    # for j in jobs:
    #     j.start()
    #
    # for i in jobs:
    #     i.join()


