import sys
import subprocess
from index import Indexer
from grapheme import build_grapheme_confusion_mtx


output_file_header = "<kwslist kwlist_filename=\"IARPA-babel202b-v1.0d_conv-dev.kwlist.xml\" language=\"swahili\" system_id=\"\">"

grapheme_file = None


def run_kws(input_file, query_file, output_file, score_norm=False, gamma=1.0):
    indexer = Indexer(grapheme_file=grapheme_file)
    indexer.build_index(input_file)

    try:
        out = open(output_file, 'w')
    except Exception as e:
        print("Error: unable to open output file.", e)
        return None

    with open(query_file, 'r') as f:
        # writing output file header
        out.write(output_file_header+'\n')
        # reading queries from query file and searching them
        for line in f.readlines():
            if 'kwid' in line:
                # getting query id
                kwid = line[line.find("=")+1 : -2] # -2 to ignore final '>' and '\n'
            if 'kwtext' in line:
                # searching for query using the indexer
                query = line[line.find("<kwtext>")+len("<kwtext>") : line.find("</kwtext>")]
                hits = indexer.search_query(query, score_norm=score_norm, gamma=gamma)
                # write query header including query id
                hit_header = "<detected_kwlist kwid={} oov_count=\"0\" search_time=\"0.0\">".format(kwid)
                out.write(hit_header+'\n')
                # writing every hit
                for hit in hits:
                    hit_str = "<kw file=\"{}\" channel=\"{}\" tbeg=\"{}\" dur=\"{}\" score=\"{}\" decision=\"YES\"/>".format(
                                    hit[0], hit[2], hit[3], hit[4], hit[5])
                    out.write(hit_str+'\n')
                
                # write query closing including query id
                out.write("</detected_kwlist>\n")

        # writing output file closing
        out.write("</kwslist>\n")



if __name__ == '__main__':

    if len(sys.argv) > 3:
        input_file = sys.argv[1]
        query_file = sys.argv[2]
        output_file = sys.argv[3]
    else:
        input_file = './lib/ctms/reference.ctm'
        query_file = './lib/kws/queries.xml'
        output_file = './output/out_reference.xml'

    # grapheme confusion matrix
    if '-graph' in sys.argv:
        grapheme_file = './lib/kws/grapheme.map'

    # keywork spotting
    if '-score_norm' in sys.argv:
        gamma = float(sys.argv[-1])
        run_kws(input_file, query_file, output_file, score_norm=True, gamma=gamma)
    else:
        run_kws(input_file, query_file, output_file)

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


# Examples:
    # python3 keyword_spotting.py ./lib/ctms/reference.ctm ./lib/kws/queries.xml ./output/out_reference.xml -sc -twv
    # python3 keyword_spotting.py ./lib/ctms/decode.ctm ./lib/kws/queries.xml ./output/out_decode.xml -sc -twv
    # python3 keyword_spotting.py ./output/morph/my_decode_morph.ctm ./output/morph/my_queries_morph.xml ./output/out_my_morph_decode.xml -sc -twv
    # python3 keyword_spotting.py ./lib/ctms/decode-morph.ctm ./output/morph/my_queries_morph.xml ./output/out_decode-morph.xml -sc -twv
    # python3 keyword_spotting.py ./lib/ctms/decode.ctm ./lib/kws/queries.xml ./output/out_decode_scNorm1.xml -sc -twv -score_norm 1.0
    # python3 keyword_spotting.py ./output/morph/my_decode_morph.ctm ./output/morph/my_queries_morph.xml ./output/out_my_morph_decode_scNorm1.xml -sc -twv -score_norm 1.0
    # python3 keyword_spotting.py ./lib/ctms/decode-morph.ctm ./output/morph/my_queries_morph.xml ./output/out_decode-morph_scNorm1.xml -sc -twv -score_norm 1.0
