def filter_map_mean(newtwork, filter_dic):

    outfile = open(newtwork.replace('.', 'EdgeFmean.'), 'w')

    with open(newtwork) as open_net:

        first_line = True

        for line in open_net:

            if first_line:

                first_line = False

                outfile.write(line)
                continue

            split_line = line.strip().split('\t')

            if split_line[2] == 'miRNA':
                outfile.write(line)
                continue

            elif float(split_line[-1]) < filter_dic[split_line[1]]['mean_weight']:

                continue

            else:

                outfile.write(line)


def filter_map_median(newtwork, filter_dic):

    outfile = open(newtwork.replace('.', 'EdgeFmed.'), 'w')

    with open(newtwork) as open_net:

        first_line = True

        for line in open_net:

            if first_line:

                first_line = False

                outfile.write(line)
                continue

            split_line = line.strip().split('\t')

            if split_line[2] == 'miRNA':
                outfile.write(line)
                continue

            elif float(split_line[-1]) < filter_dic[split_line[1]]['median_weight']:

                continue

            else:

                outfile.write(line)


def filter_map_2SDmeanH(newtwork, filter_dic):

    """

    :param newtwork:
    :param filter_dic:
    :return:

    Filters the network removing anything below 2SD of the mean

    """

    outfile = open(newtwork.replace('.', 'EdgeFmean2SDoM.'), 'w')

    with open(newtwork) as open_net:

        first_line = True

        for line in open_net:

            if first_line:

                first_line = False

                outfile.write(line)

            split_line = line.strip().split('\t')

            if split_line[2] == 'miRNA':
                outfile.write(line)
                continue

            elif float(split_line[-1]) < filter_dic[split_line[1]]['mean_weight']-(2*filter_dic[split_line[1]]['SD_weight']):

                continue

            else:

                outfile.write(line)


def filter_map_1SDmeanH(newtwork, filter_dic):

    """

    :param newtwork:
    :param filter_dic:
    :return:

    Filters the network removing anything below 2SD of the mean

    """

    outfile = open(newtwork.replace('.', 'EdgeF_1D2SM.'), 'w')

    with open(newtwork) as open_net:

        first_line = True

        for line in open_net:

            if first_line:

                first_line = False

                outfile.write(line)

            split_line = line.strip().split('\t')

            if split_line[2] == 'miRNA':
                outfile.write(line)
                continue

            elif float(split_line[-1]) < filter_dic[split_line[1]]['mean_weight']-(filter_dic[split_line[1]]['SD_weight']):

                continue

            else:
                # print(filter_dic[split_line[1]]['mean_weight']-(filter_dic[split_line[1]]['SD_weight']))
                outfile.write(line)


def filter_map_2SDmeanBW(newtwork, filter_dic):

    """

    :param newtwork:
    :param filter_dic:
    :return:

    Filters the network removing anything below or above 2SD of the mean

    """

    outfile = open(newtwork.replace('.', 'EdgeF_2D2SM.'), 'w')

    with open(newtwork) as open_net:

        first_line = True

        for line in open_net:

            if first_line:
                first_line = False

                outfile.write(line)

            split_line = line.strip().split('\t')

            if split_line[2] == 'miRNA':
                outfile.write(line)
                continue

            elif float(split_line[-1]) < filter_dic[split_line[1]]['mean_weight'] - (
                    2 * filter_dic[split_line[1]]['SD_weight']):

                continue

            elif float(split_line[-1]) > filter_dic[split_line[1]]['mean_weight'] + (
                    2 * filter_dic[split_line[1]]['SD_weight']):

                continue

            else:

                outfile.write(line)


def load_filter_dic(edge_stats):

    edge_dic = {}
    head_line = []

    with open(edge_stats) as edge_open:

        first_line = True

        for line in edge_open:

            if first_line:

                first_line = False
                head_line = line.strip().split('\t')
                continue

            split_line = line.strip().split('\t')
            print(split_line[0])
            edge_dic[split_line[0]] = {}

            for x in range(1, len(head_line)):

                edge_dic[split_line[0]][head_line[x]] = float(split_line[x])



    return edge_dic


if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('network')

    parser.add_argument('edge_stats')

    args = parser.parse_args()

    filter_dic = load_filter_dic(args.edge_stats)

    filter_map_2SDmeanH(args.network, filter_dic)
    # filter_map_2SDmeanBW(args.network, filter_dic)
    # filter_map_1SDmeanH(args.network, filter_dic)
    # filter_map_mean(args.network, filter_dic)
    # filter_map_median(args.network, filter_dic)
