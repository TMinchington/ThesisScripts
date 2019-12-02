"""
in_out vs autoregulate
"""

def load_auto_vs_non_auto(motif_dir):
    
    import os

    file_path = os.path.join(motif_dir, 'auto_vs_no_auto.txt') 
    auto_dic = {}
    with open(file_path) as auto_non_open:
        for line in auto_non_open:
            gene, autoreg = line.strip().split('\t')
            auto_dic[gene] = autoreg
    
    return auto_dic.copy()

motif_dir = '/Users/mqbpktm3/Dropbox (The University of Manchester)/0-PhD/1-ChIP Network/20-Final_net_numbers/fast_motifs/'
network = '/Users/mqbpktm3/Dropbox (The University of Manchester)/0-PhD/1-ChIP Network/20-Final_net_numbers/REMAP2018_mapdd_select-collapsed_ctmEdgeFmean2SDoM-fixed_mirs.txt'
outfile = open('/Users/mqbpktm3/Dropbox (The University of Manchester)/0-PhD/1-ChIP Network/20-Final_net_numbers/fast_motifs/graphs/edge_counts_by_auto.tsv', 'w')
auto_dic = load_auto_vs_non_auto(motif_dir)

gene_dic_out = {}
gene_dic_in = {}
tr = {}

with open(network) as open_net:
    for line in open_net:
        split_line = line.strip().split('\t')
        # print(split_line)
        reg = split_line[1]
        reg_type = split_line[2]
        target = split_line[4]
        target_type = split_line[5]

        if reg_type == 'protein_coding':
            tr[reg] = 0
        # print(target_type)
        # exit()
        if target_type not in ['miRNA', 'protein_coding']:
            continue
        
        try:
            gene_dic_out[reg][target_type] += 1
        except KeyError:
            try:
                gene_dic_out[reg][target_type] = 1
            except KeyError:
                gene_dic_out[reg] = {target_type: 1}

        
        try:
            gene_dic_in[target][reg_type] += 1

        except KeyError:
            try:
                gene_dic_in[target][reg_type] = 1
            except KeyError:
                gene_dic_in[target] = {reg_type: 1}

print(gene_dic_in)
print(gene_dic_out)
outfile.write('trx\tgene_type\tin_count\tout_count\tauto_dic[trx]\n')
for trx in tr:
    for gene_type in gene_dic_out[trx]:

        try:
            in_count = gene_dic_in[trx][gene_type]

        except KeyError:
            in_count = 0

        try:
            out_count = gene_dic_out[trx][gene_type]

        except KeyError:
            out_count = 0

        outfile.write(f'{trx}\t{gene_type}\t{in_count}\t{out_count}\t{auto_dic[trx]}\n')

outfile.close()