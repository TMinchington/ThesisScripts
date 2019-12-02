"""
New Tissue Map 2019
"""

def load_cello2_tissues_to_cells(cello_path):

    tiss_dic = {}

    with open(cello_path) as ocello:
        for line in ocello:
            split_line = line.strip().split('\t')
            try:
                tiss_dic[split_line[0]].append(split_line[1])
            except KeyError:
                tiss_dic[split_line[0]] = [split_line[1]]

    return tiss_dic


def make_tissue_nets(network_file):
    from pprint import pprint
    import os
        
    for tissue in cello_dic:
        
        
        tissue_path = os.path.join(tissue_folder, tissue)

        if not os.path.isdir(tissue_path):
            os.makedirs(tissue_path)

        outfile = open(os.path.join(tissue_path, tissue+'_network.txt'), 'w')
        with open(network_file) as open_net:
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

                elif split_line[5] not in ['protein_coding', 'miRNA']:
                    continue

                cells_ls = [x.split('_')[0] for x in split_line[-2].split(' ')]

                compare_ls = [x for x in cells_ls if x in cello_dic[tissue]]

                if len(compare_ls) != 0:
                    outfile.write(line)
                    # print(line)
                    continue

                else:
                    # print(line)
                    continue


if __name__ == "__main__":
    
    import os
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("celloframe2")
    parser.add_argument("network")
    args = parser.parse_args()

    tissue_folder = os.path.join(os.path.split(args.network)[0], 'tissues')

    if not os.path.isdir(tissue_folder):
        os.makedirs(tissue_folder)

    cello_dic = load_cello2_tissues_to_cells(args.celloframe2)
    # print(cello_dic)
    make_tissue_nets(args.network)

