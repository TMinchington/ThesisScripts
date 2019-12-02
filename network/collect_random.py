from sys import argv
import os

directory = argv[1]
outdir = argv[1]+'_master'

if not os.path.isdir(outdir):

    os.makedirs(outdir)

folder_ls = [x for x in os.listdir(directory) if '.' not in x and 'ran_map' in x]

amp_master = open('{}/amp_fb_new_master.txt'.format(outdir), 'w')
dual_amp_master = open('{}/dual_amp_fb_master.txt'.format(outdir), 'w')
gene_fb_mir_master = open('{}/genes_fb__mir_master.txt'.format(outdir), 'w')
gene_mir_self_master = open('{}/genes_mir_self_master.txt'.format(outdir), 'w')
tf_mir_tf_master = open('{}/tf_mir_tf_master.txt'.format(outdir), 'w')
# simple_mo_master = open('{}/simple_mo_master.txt'.format(outdir), 'w')
mo_sum_master = open('{}/summary_master.txt'.format(outdir), 'w')
# mir_mo_master = open('{}/mir_motifs_master.txt'.format(outdir), 'w')

# print(folder_ls)
for folder in folder_ls:

    motif_dir = '{}/{}/fast_motifs'.format(directory, folder)
    # stat_dir = '{}/{}/stat'.format(directory, folder)

    amp = open('{}/amplified_fb.txt'.format(motif_dir))

    for line in amp:

        amp_master.write(folder)
        amp_master.write('\t')
        amp_master.write(line)

    amp.close()

    damp = open('{}/dual_fb.txt'.format(motif_dir))

    for line in damp:

        dual_amp_master.write(folder)
        dual_amp_master.write('\t')
        dual_amp_master.write(line)

    damp.close()

    gfbm = open('{}/inc_fb.txt'.format(motif_dir))

    for line in gfbm:

        gene_fb_mir_master.write(folder)
        gene_fb_mir_master.write('\t')
        gene_fb_mir_master.write(line)

    gfbm.close()

    gms = open('{}/target_host.txt'.format(motif_dir))

    for line in gms:

        gene_mir_self_master.write(folder)
        gene_mir_self_master.write('\t')
        gene_mir_self_master.write(line)

    gms.close()

    tfmtf = open('{}/tf-mir-tf.txt'.format(motif_dir))

    for line in tfmtf:

        tf_mir_tf_master.write(folder)
        tf_mir_tf_master.write('\t')
        tf_mir_tf_master.write(line)

    tfmtf.close()

    mo_sum = open('{}/motif_summary.txt'.format(motif_dir))

    for line in mo_sum:
        # print(line)
        mo_sum_master.write(folder+'\t'+line)

    mo_sum.close()

    # mir_mo = open('{}/mir_motifs.txt'.format(motif_dir))

    # for line in mir_mo:
    #     print(line)
    #     mir_mo_master.write(folder+'\t'+line)
    #
    # mir_mo.close()


amp_master.close()
dual_amp_master.close()
gene_fb_mir_master.close()
gene_mir_self_master.close()
tf_mir_tf_master.close()
# mir_mo_master.close()
# simple_mo_master.close()
