

def read_morph_dict(morph_file):
    morph_dict = {}
    with open(morph_file, 'r') as f:
        for line in f.readlines():
            if len(line) > 1:
                tokens = line.split()
                if len(tokens) < 2:
                    print("Error: invalid format morph decomp. file")
                    return None
                
                word = tokens[0].lower()
                morphemes = tokens[1:]
                morphemes = [item.lower() for item in morphemes]

                if word in morph_dict and morph_dict[word] != morphemes:
                    print("Warning: the word {} appears more than once in morph file with different decompositions:".format(word))
                else:
                    morph_dict[word] = morphemes
    
    return morph_dict



def morph_decode_infile(input_file, morph_file, output_file):

    morph_dict = read_morph_dict(morph_file)

    try:
        out = open(output_file, 'w')
    except Exception as e:
        print("Error: unable to open output file.", e)
        return None

    with open(input_file, 'r') as f:
        for line in f.readlines():
            if len(line) > 1:
                tokens = line.split()
                # retrieving token information
                doc_id = tokens[0]
                ch = tokens[1]
                tbeg = tokens[2]
                dur = tokens[3]
                word = tokens[4].lower()
                score = tokens[5]

                if word in morph_dict:
                    # splitting total duration depeding on the number of morphemes
                    new_dur = float(dur)/len(morph_dict[word])
                    prev_tbeg = float(tbeg)
                    for morph in morph_dict[word]:
                        new_line = doc_id+' '+ch+' '+str(round(prev_tbeg,2))+' '+str(round(new_dur,2))+' '+morph+' '+score+'\n'
                        prev_tbeg += round(new_dur,2)
                        out.write(new_line)

                else:
                    out.write(line)



def morph_decode_queryfile(query_file, morph_file, output_file):

    morph_dict = read_morph_dict(morph_file)

    try:
        out = open(output_file, 'w')
    except Exception as e:
        print("Error: unable to open output file.", e)
        return None

    with open(query_file, 'r') as f:
        for line in f.readlines():
            if len(line) > 1:
                if 'kwtext' in line:
                    query = line[line.find("<kwtext>")+len("<kwtext>") : line.find("</kwtext>")]
                    query_list = query.split()
                    new_query = ''
                    for word in query_list:
                        word = word.lower()
                        if word in morph_dict:
                            morph_word = ' '.join(morph_dict[word])
                            new_query += morph_word+' '
                        else:
                            new_query += word + ' '
                        
                    new_query = new_query[:-1] # deleting final ' '
                    new_line = line[:line.find("<kwtext>")+len("<kwtext>")] +new_query+line[line.find('</kwtext>'):]
                    out.write(new_line)
                else:
                    out.write(line)




if __name__ == '__main__':
    input_infile = './lib/ctms/decode.ctm'
    morph_infile = './lib/dicts/morph.dct'
    output_infile = './output/morph/my_decode_morph.ctm'

    input_qfile = './lib/kws/queries.xml'
    morph_qfile = './lib/dicts/morph.kwslist.dct'
    output_qfile = './output/morph/my_queries_morph.xml'

    morph_decode_infile(input_infile, morph_infile, output_infile)

    morph_decode_queryfile(input_qfile, morph_qfile, output_qfile)

