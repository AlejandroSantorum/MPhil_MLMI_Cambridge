

class Indexer:

    def __init__(self):
        self.word_index = {}
        self.doc_index = {}


    def _update_word_index(self, word, doc_id, word_position):
        info = (doc_id, word_position)

        if word in self.word_index:
            self.word_index[word].append(info)
        else:
            self.word_index[word] = [info]
    

    def _update_doc_index(self, doc_id, word, channel, tbeg, dur, score):
        info = (word, int(channel), float(tbeg), float(dur), float(score))

        if doc_id in self.doc_index:
            self.doc_index[doc_id].append(info)
        else:
            self.doc_index[doc_id] = [info]

    
    def build_index(self, input_file):
        with open(input_file, 'r') as f:
            prev_doc = ''    # previous analyzed document id
            position = None  # position of the word in the document
            for line in f.readlines():
                if len(line)>1: # valid line
                    tokens = line[:-1].split(' ')
                    if len(tokens) != 6: # incorrect format
                        print("Format error: the input file has the incorrect format")
                        return None

                    # retrieving token information
                    doc_id = tokens[0]
                    channel = tokens[1]
                    tbeg = tokens[2]
                    dur = tokens[3]
                    word = tokens[4]
                    score = tokens[5]
                    
                    # update position of the word in the document
                    if prev_doc == doc_id:
                        position += 1
                    else:
                        position = 0
                    # update previous doc_id
                    prev_doc = doc_id

                    # updating word and doc indices
                    self._update_word_index(word, doc_id, position)
                    self._update_doc_index(doc_id, word, channel, tbeg, dur, score)


    def _calculate_score(self, doc_id, word_position, query_length):
        score = 0.0
        for i in range(query_length):
            score += self.doc_index[doc_id][word_position+i][4]
        return score/query_length


    def search_query(self, query):
        if self.word_index is None or self.doc_index is None:
            print("Error: index not initialized. Execute build_index() specifying an input file")
            return None
        
        query_words = query.split(' ')
        if len(query_words) < 1:
            print("Error: invalid query")
            return None
        
        ret = []
        word0 = query_words[0]
        for doc_id, word_position in self.word_index[word0]:
            # prev_end_time = prev_tbeg + prev_dur
            prev_end_time = self.doc_index[doc_id][word_position][2]+self.doc_index[doc_id][word_position][3]
            hit = True # hit flag  
            for i in range(1, len(query_words)):
                # checking phrase in the document
                if self.doc_index[doc_id][word_position+i][0] == query_words[i]:
                    # checking time condition (1/2 second rule)
                    if self.doc_index[doc_id][word_position+i][2] - 0.5 <= prev_end_time:
                        # prev_end_time = prev_tbeg + prev_dur
                        prev_end_time = self.doc_index[doc_id][word_position+i][2] + self.doc_index[doc_id][word_position+i][3]
                else:
                    hit = False
                    break
            
            if hit:
                # word 0
                ret_word = self.doc_index[doc_id][word_position][0]
                # channel of word 0
                ret_ch = self.doc_index[doc_id][word_position][1]
                # beginning time of word 0
                ret_tbeg = self.doc_index[doc_id][word_position][2]
                # total duration of phrase = last word beg_time + last word dur - first word beg_time
                ret_dur = self.doc_index[doc_id][word_position+len(query_words)-1][2] + \
                            self.doc_index[doc_id][word_position+len(query_words)-1][3] - ret_tbeg
                ret_dur = round(ret_dur, 2)
                # score
                ret_score = self._calculate_score(doc_id, word_position, len(query_words))
                # query hit information
                ret_item = (doc_id, ret_word, ret_ch, ret_tbeg, ret_dur, ret_score)
                ret.append(ret_item)

        return ret



                
    



if __name__ == '__main__':
    indexer = Indexer()
    indexer.build_index('./lib/ctms/reference.ctm')

    print(indexer.search_query('nimwachie'))
    # expected output:
    #   file="BABEL_OP2_202_92740_20130923_235638_outLine" channel="1" tbeg="104.61" dur="0.75" score="1.000000"

    #print(indexer.search_query('what'))

    print(indexer.search_query('what she has gone'))
    # expected output:
    #   file="BABEL_OP2_202_29663_20131208_035816_outLine" channel="1" tbeg="217.41" dur="0.83" score="1.000000"