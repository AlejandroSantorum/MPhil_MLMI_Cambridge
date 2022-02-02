from index import Indexer


output_file_header = "<kwslist kwlist_filename=\"IARPA-babel202b-v1.0d_conv-dev.kwlist.xml\" language=\"swahili\" system_id=\"\">"


def run_kws(input_file, query_file, output_file):
    indexer = Indexer()
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
                hits = indexer.search_query(query)
                # write query header including query id
                hit_header = "<detected_kwlist kwid={} oov_count=\"0\" search_time=\"0.0\">".format(kwid)
                out.write(hit_header+'\n')
                # writing every hit
                for hit in hits:
                    hit_str = "<kw file=\"{}\" channel=\"{}\" tbeg=\"{}\" dur=\"{}\" score=\"{:.5f}\" decision=\"YES\"/>".format(
                                    hit[0], hit[2], hit[3], hit[4], round(hit[5],5))
                    out.write(hit_str+'\n')
                
                # write query closing including query id
                out.write("</detected_kwlist>\n")

        # writing output file closing
        out.write("</kwslist>\n")



if __name__ == '__main__':

    input_file = './lib/ctms/reference.ctm'
    query_file = './lib/kws/queries.xml'
    output_file = './test_output.xml'

    run_kws(input_file, query_file, output_file)
    

    
