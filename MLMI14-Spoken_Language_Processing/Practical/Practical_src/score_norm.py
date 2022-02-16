import sys
import subprocess
import numpy as np


def format_batch_lines(batch_lines, new_scores):
    format_lines = []
    
    assert len(batch_lines) == len(new_scores)

    for idx, line in enumerate(batch_lines):
        new_line = line[:line.find('score=\"')+len('score=\"')] + str(new_scores[idx]) + line[line.find('\" decision'):]
        format_lines.append(new_line)
    
    return format_lines



def run_score_norm(scores):
    npscores = np.array(scores)
    # print(npscores)
    return npscores/np.sum(npscores)



def score_normalisation(file_to_norm, out_file):
    fout = open(out_file, 'w')

    with open(file_to_norm, 'r') as f:
        for line in f.readlines():
            if '<detected_kwlist' in line:
                scores = []
                batch_lines = []
                fout.write(line)
            elif '<kw file=' in line:
                batch_lines.append(line)
                sc = line[line.find('score=\"')+len('score=\"'):line.find('\" decision')]
                scores.append(float(sc))
            elif '</detected_kwlist>' in line:
                normed_scores = run_score_norm(scores)
                format_lines = format_batch_lines(batch_lines, normed_scores)
                for l in format_lines:
                    fout.write(l)
                fout.write(line)
            else:
                fout.write(line)



if __name__ == '__main__':
    if len(sys.argv) > 3:
        file_to_norm = sys.argv[1]
        output_file = sys.argv[2]
    elif len(sys.argv) == 3 and ('-sc' not in sys.argv) and ('-twv' not in sys.argv):
        file_to_norm = sys.argv[1]
        output_file = sys.argv[2]
    else:
        file_to_norm = './lib/kws/morph-test.xml'
        output_file = './lib/kws/morph-test_scNorm.xml'

    score_normalisation(file_to_norm, output_file)

    # scoring if specified
    if '-sc' in sys.argv:
        cmd = "scripts/score.sh {} scoring".format(output_file)
        process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        if error:
            print(error)
            exit()
    
    # get TWV
    if '-twv' in sys.argv:
        # whole system performance
        cmd = "./scripts/termselect.sh lib/terms/ivoov.map {} scoring all".format(output_file)
        process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        print(output[:-1].decode())
        # IV performance
        cmd = "./scripts/termselect.sh lib/terms/ivoov.map {} scoring iv".format(output_file)
        process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        print(output[:-1].decode())
        # OOV performance
        cmd = "./scripts/termselect.sh lib/terms/ivoov.map {} scoring oov".format(output_file)
        process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        print(output[:-1].decode())
