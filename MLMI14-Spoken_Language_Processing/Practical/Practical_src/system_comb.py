import sys
import subprocess
import numpy as np


def combine_systems(list_out_files, sys_weights):
    # dictionary of dictionaries. Root dictionary indexed by
    #   query ID (kwid), and all the nested dictionaries are
    #   indexed by file_id+'_'+tbeg, identifying a query hit.
    comb_dict = {}

    # Looping through all output files to combine them
    for sys_idx, file_name in enumerate(list_out_files):
        with open(file_name, 'r') as f:
            for line in f.readlines():
                # identifying query by kwid
                if '<detected_kwlist' in line:
                    kwid = line[line.find('=')+1 : line.find(' oov_count')]
                    if kwid not in comb_dict:
                        comb_dict[kwid] = {}
                # identifying a hit inside a query by file_id + tbeg
                elif 'kw file' in line:
                    file_id = line[line.find('file=')+len('file=') : line.find(' channel')]
                    channel = line[line.find('channel=')+len('channel=') : line.find(' tbeg')]
                    tbeg = line[line.find('tbeg=')+len('tbeg=') : line.find(' dur')]
                    dur = line[line.find('dur=')+len('dur=') : line.find(' score')]
                    score = float(line[line.find('score=\"')+len('score=\"') : line.find('\" decision')])

                    hit_key = file_id + '_' + tbeg
                    if hit_key in comb_dict[kwid]:
                        # actual system combination procedur
                        comb_dict[kwid][hit_key][4] += sys_weights[sys_idx]*score

                    else:
                        # just adding the hit to the query dict
                        comb_dict[kwid][hit_key] = [file_id, channel, tbeg, dur, sys_weights[sys_idx]*score]
    
    return comb_dict



output_file_header = "<kwslist kwlist_filename=\"IARPA-babel202b-v1.0d_conv-dev.kwlist.xml\" language=\"swahili\" system_id=\"\">"

def write_output(output_file, comb_dict):
    with open(output_file, 'w') as f:
        f.write(output_file_header+'\n')

        for kwid in comb_dict:
            hit_header = "<detected_kwlist kwid={} oov_count=\"0\" search_time=\"0.0\">".format(kwid)
            f.write(hit_header+'\n')

            for hit_key in comb_dict[kwid]:
                hit_str = "<kw file={} channel={} tbeg={} dur={} score=\"{:.5f}\" decision=\"YES\"/>".format(
                                        comb_dict[kwid][hit_key][0], comb_dict[kwid][hit_key][1], comb_dict[kwid][hit_key][2],
                                        comb_dict[kwid][hit_key][3], comb_dict[kwid][hit_key][4])
                f.write(hit_str+'\n')
            
            f.write("</detected_kwlist>\n")
        f.write("</kwslist>\n")


def _read_mtwv(output_file):
    # parsing output file
    output_name = output_file.split('/')[-1]
    output_name = output_name[:output_name.find('.')]

    with open('./scoring/'+output_name+'-res.txt', 'r') as f:
        res_line = f.readlines()[-1]
        mtwv = float(res_line.split('|')[16])

    return mtwv


def main():
    if len(sys.argv) == 2 and sys.argv[1] == 'default':
        sys_outfiles = ['./lib/kws/word.xml', './lib/kws/word-sys2.xml']
        comb_out_file = './test_sys_comb.xml'
        sys_weights = np.ones(len(sys_outfiles))

    elif len(sys.argv) < 5:
        print("Error: insufficient input parameters.")
        print("Include, at least two output files to combine, the output path and the combination mode.")
        return
    
    else:
        sys_comb_mode = sys.argv[-1] # combination mode
        comb_out_file = sys.argv[-2] # output file after system combination procedure
        sys_outfiles = sys.argv[1:-2] # path of files to combine
            
        if sys_comb_mode == '-combSUM' or sys_comb_mode == '-combsum':
            # basically no weights
            sys_weights = np.ones(len(sys_outfiles))

        elif sys_comb_mode == '-combMEAN' or sys_comb_mode == '-combmean':
            # all systems are equally weighted, summing up to 1
            sys_weights = 1/len(sys_outfiles) * np.ones(len(sys_outfiles))
        
        elif sys_comb_mode == '-WcombSUM' or sys_comb_mode == '-wcombsum':
            mtwvs = []
            for file in sys_outfiles:
                mtwvs.append(_read_mtwv(file))
            # systems are weighted depending on their MTWV
            sys_weights = np.array(mtwvs)/np.sum(np.array(mtwvs))

    comb_dict = combine_systems(sys_outfiles, sys_weights)
    write_output(comb_out_file, comb_dict)

    # scoring results
    cmd = "scripts/score.sh {} scoring".format(comb_out_file)
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    if error:
        print(error)
        exit()

    # whole system performance
    cmd = "./scripts/termselect.sh lib/terms/ivoov.map {} scoring all".format(comb_out_file)
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    print(output[:-1].decode())
    # IV performance
    cmd = "./scripts/termselect.sh lib/terms/ivoov.map {} scoring iv".format(comb_out_file)
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    print(output[:-1].decode())
    # OOV performance
    cmd = "./scripts/termselect.sh lib/terms/ivoov.map {} scoring oov".format(comb_out_file)
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    print(output[:-1].decode())



if __name__ == '__main__':
    main()

    # EXAMPLES:
        # python3 system_comb.py ./lib/kws/word.xml ./lib/kws/word-sys2.xml ./test_sys_comb.xml -combSUM
        # python3 system_comb.py ./lib/kws/word.xml ./lib/kws/word-sys2.xml ./test_sys_comb.xml -combMEAN

        # python3 system_comb.py ./output/out_decode.xml ./output/out_my_morph_decode.xml ./output/sys_combination/decode+my_decode_morph.xml -combSUM