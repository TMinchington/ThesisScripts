# file to convert mirTarBase to seed vicious output

from sys import argv

mirTar_file = open(argv[1])

hsa_high_conf = open(argv[2]) # mature listed

ensembl = open(argv[3])

outfile = open(argv[4], 'w')
outfile2 = open(argv[4].replace('.txt', '_no_match.txt'), 'w')


mir_base_dic = {}
hit_list = []

for line in hsa_high_conf:

    if line.startswith('microRNA'):
        continue

    line = line.strip()
    line = line.split('\t')

    mir_base_dic[line[0]] = line[1]

    # print(line[0])

gene_names = {}
found_ls = []
hit_list = list(mir_base_dic)

for line in ensembl:

    if line.startswith('Ensembl'):

        continue

    line = line.strip()
    line = line.split('\t')

    if line[2] in found_ls:

        continue

    gene_names[line[2]] = [line[0], line[1], line[7]]



for line in mirTar_file:

    if line.startswith('miRTarBase'):

        continue

    line = line.strip()
    line = line.split('\t')

    if line[1] not in hit_list:

        print(line)



        continue

    mir_name = line[1]

    try:

        mimat = mir_base_dic[mir_name]

    except KeyError:

        outfile2.write('mirbase\t')
        outfile2.write(mimat)
        outfile2.write('\n')
        # print(mimat)
        continue

    gene_name = line[3]


    try:

        ens_gen_code = gene_names[gene_name][0]

    except KeyError:

        outfile2.write('ensembl\t')
        outfile2.write(gene_name)
        outfile2.write('\n')
        # print(gene_name)
        continue

    ens_trans_code = gene_names[gene_name][1]
    ens_gen_type = gene_names[gene_name][2]



    outfile.write('{}|{}|{}|{}|na\tF\t{} {}\t0\tmiranda\n'.format(ens_gen_code, ens_trans_code, gene_name, ens_gen_type, mir_name, mimat))




# print(list(mir_base_dic))




