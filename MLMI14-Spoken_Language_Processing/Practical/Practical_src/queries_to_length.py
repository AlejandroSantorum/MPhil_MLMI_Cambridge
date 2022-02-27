import numpy as np


def main(query_file, output_file):
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


if __name__ == '__main__':
    query_file = './lib/kws/queries.xml'
    output_file = './lib/terms/length.map'

    main(query_file, output_file)