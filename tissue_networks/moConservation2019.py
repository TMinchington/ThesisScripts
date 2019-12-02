"""
Motif conservation 2019
"""

def check_which_tf_in_tissue(tissue_dir):

    import os
    from pprint import pprint as pp
    tissue_dic = {}
    tissues_ls = [x for x in os.listdir(tissue_dir) if not '.' in x]

    for tissue in tissues_ls:
        tissue_path = os.path.join(tissue_dir, tissue, tissue+"_network.txt")

        if not os.path.isfile(tissue_path):
            continue
        first_line = True
        with open(tissue_path) as o_net:
            for line in o_net:
                if first_line:
                    first_line = False
                    continue

                split_line = line.strip().split('\t')

                try:
                    tissue_dic[split_line[1]][tissue]=0

                except KeyError:
                    tissue_dic[split_line[1]] = {tissue: 0}

    pp(tissue_dic)


def conserved_protein_targets(tissue_dir):

    import os
    from pprint import pprint as pp
    target_dic = {}
    tissue_dic = {}
    tissues_ls = [x for x in os.listdir(tissue_dir) if not '.' in x]

    outfile = open(tissue_dir+'/conserved_interactions.txt', 'w')
    outfile.write(f'regulator\ttarget\ttarget_type\ttissues_expressed\tinteraction_seen\tperc_conservation\n')
    for tissue in tissues_ls:
        tissue_path = os.path.join(tissue_dir, tissue, tissue+"_network.txt")

        if not os.path.isfile(tissue_path):
            continue
        first_line = True
        with open(tissue_path) as o_net:
            for line in o_net:
                if first_line:
                    first_line = False
                    continue

                (regulator, regulator_name, reg_type, target, 
                target_name, target_type, score, distance_act, 
                distance_abs, experiment, cell, count)  = line.strip().split('\t')

                if not reg_type == "protein_coding":
                    continue

                try:
                    target_dic[regulator_name][target_type][target_name][tissue] = 0

                except KeyError:
                    try:
                        target_dic[regulator_name][target_type][target_name] = {tissue: 0}

                    except KeyError:
                        try:   
                            target_dic[regulator_name][target_type] = {target_name: {tissue: 0}}

                        except KeyError:
                            target_dic[regulator_name] = {target_type: {target_name: {tissue: 0}}}

                try:
                    tissue_dic[regulator_name][tissue]=0

                except KeyError:
                    tissue_dic[regulator_name] = {tissue: 0}

        
    for regulator in tissue_dic:
        if len(tissue_dic[regulator]) <= 1:
            continue
        for target_type in target_dic[regulator]:
            if target_type not in ['protein_coding', 'miRNA']:
                continue
            for target in target_dic[regulator][target_type]:
                
                outfile.write(f'{regulator}\t{target}\t{target_type}\t{len(tissue_dic[regulator])}\t{len(target_dic[regulator][target_type][target])}\t{len(target_dic[regulator][target_type][target])/len(tissue_dic[regulator])}\n')

    outfile.close()
    # pp(tissue_dic)



if __name__ == "__main__":
    
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("tissue_dir")

    args = parser.parse_args()

    # tissue_dic = check_which_tf_in_tissue(args.tissue_dir)
    conserved_protein_targets(args.tissue_dir)