import numpy as np
import subprocess


def build_map_file(query_file, output_file):
    fout = open(output_file, 'w')

    # Maximum length of a query.
    # For this practical it is known it is 5
    counters = [0]*5

    with open(query_file, 'r') as f:
        for line in f.readlines():
            if 'kw kwid' in line:
                kwid = line[line.find('-')+1 : line.find("\">")]
            elif 'kwtext' in line:
                query = line[line.find('<kwtext>')+len('<kwtext>') : line.find('</kwtext>')]
                length = len(query.split())
                if length == 1:
                    map_word = 'one'
                elif length == 2:
                    map_word = 'two'
                elif length == 3:
                    map_word = 'three'
                elif length == 4:
                    map_word = 'four'
                elif length == 5:
                    map_word = 'five'
                else:
                    print("Error: query with length greater than 5")
                    return None

                out_line = map_word+' '+str(kwid)+' '+str(counters[length-1]).zfill(4)+'\n'
                counters[length-1] += 1
                fout.write(out_line)
    
    print("====Percentages====:")
    s = sum(np.array(counters))
    for i in range(5):
        print("Queue length "+str(i+1)+":", counters[i]/s)



def score_files(scoring_files):
    for file in scoring_files:
        print("===>", file)
        for i in range(5):
            if i == 0:
                termselect = 'one'
            elif i == 1:
                termselect = 'two'
            elif i == 2:
                termselect = 'three'
            elif i == 3:
                termselect = 'four'
            elif i == 4:
                termselect = 'five'

            cmd = "./scripts/termselect.sh lib/terms/length.map {} scoring {}".format(file, termselect)
            process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
            output, error = process.communicate()
            print(output[:-1].decode())



if __name__ == '__main__':
    query_file = './lib/kws/queries.xml'
    output_file = './lib/terms/length.map'

    scoring_files = ['./lib/kws/morph.xml', './lib/kws/morph_SN.xml', \
                     './output/sys_comb/sum_morph_SN+word_SN.xml', \
                     './output/sys_comb/sum_decode_graph_SN+word_SN+morph_SN.xml']

    build_map_file(query_file, output_file)
    score_files(scoring_files)