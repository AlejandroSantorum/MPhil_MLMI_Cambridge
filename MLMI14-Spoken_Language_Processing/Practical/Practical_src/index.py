import sys
from Levenshtein import distance as levenshtein_distance
from difflib import SequenceMatcher
from grapheme import build_grapheme_confusion_mtx, grapheme_to_idx


class Indexer:

    def __init__(self, grapheme_file=None):
        self.word_index = {}
        self.doc_index = {}
        self.cache_scores = []
        self.grapheme_mtx = None
        if grapheme_file:
            self.grapheme_mtx = build_grapheme_confusion_mtx(grapheme_file)


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
                    tokens = line[:-1].split()
                    if len(tokens) != 6: # incorrect format
                        print("Format error: the input file has the incorrect format")
                        return None

                    # retrieving token information
                    doc_id = tokens[0]
                    channel = tokens[1]
                    tbeg = tokens[2]
                    dur = tokens[3]
                    word = tokens[4].lower()
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

    
    def _cache_scores(self, doc_id, word_position, query_length):
        cache = []
        for i in range(query_length):
            cache.append(self.doc_index[doc_id][word_position+i][4])
        self.cache_scores.append(cache)


    def _calculate_scores(self, hits, query_length, metric='mean', score_norm=False, gamma=1.0):
        ret = []
        # perform score normalisation if specified
        if score_norm:
            # calculating denominators of the score normalisation expression
            denominators = [sum([sc[i] for sc in self.cache_scores]) for i in range(query_length)]
            for i in range(len(self.cache_scores)):
                for j in range(len(self.cache_scores[i])):
                    # score normalisation
                    self.cache_scores[i][j] = (self.cache_scores[i][j]**gamma)/(denominators[j]**gamma)

        # checking all scores have been stored
        if len(hits) != len(self.cache_scores):
            print("Error: number of hits is different from the number of cached scores arrays")
            return None
        
        # calculating query score
        for idx, hit in enumerate(hits):
            if metric == 'prod':
                score = 1.0
                for sc in self.cache_scores[idx]:
                    score *= sc
            elif metric == 'mean':
                score = 0.0
                for sc in self.cache_scores[idx]:
                    score += sc
                score/=len(self.cache_scores[idx])
            else:
                print("Error: invalid metric")
                return None
            
            ret_hit = hit + (score,) # concatenating tuples
            ret.append(ret_hit)
        
        return ret
    

    def _get_closest_word_iv(self, word):
        min_dist = 1000
        min_word = None

        for w in self.word_index:
            d = levenshtein_distance(w, word)
            if d < min_dist:
                min_dist = d
                min_word = w
 
        return min_word


    def _calc_conf_prob(self, query_word, iv_word):
        # adding silences depeding on the longest matching substring
        (idx_qu, idx_iv, length) = SequenceMatcher(None, query_word, iv_word).find_longest_match(0, len(query_word), 0, len(iv_word))
        # adding silences in front
        if idx_qu > idx_iv:
            padding = ' '*(idx_qu-idx_iv)
            iv_word = padding + iv_word
        elif idx_iv > idx_qu:
            padding = ' '*(idx_iv-idx_qu)
            query_word = padding + query_word
        # adding silences at the end
        if len(query_word) > len(iv_word):
            padding = ' '*(len(query_word)-len(iv_word))
            iv_word += padding
        elif len(iv_word) > len(query_word):
            padding = ' '*(len(iv_word)-len(query_word))
            query_word += padding

        assert len(iv_word) == len(query_word)

        # calculate confusion probability
        conf_prob = 1.0
        for i in range(len(iv_word)):
            conf_prob *= self.grapheme_mtx[grapheme_to_idx(iv_word[i])][grapheme_to_idx(query_word[i])]
        
        return conf_prob



    def search_query(self, query, score_norm=False, gamma=1.0):
        if self.word_index is None or self.doc_index is None:
            print("Error: index not initialized. Execute build_index() specifying an input file")
            return None
        
        query_words = query.split()
        if len(query_words) < 1:
            print("Error: invalid query")
            return None
        
        ret = []
        conf_prob = 1.0
        word0 = query_words[0].lower()
        # first word OOV
        if word0 not in self.word_index:
            if self.grapheme_mtx is not None:
                cl_word_iv = self._get_closest_word_iv(word0)
                conf_prob *= self._calc_conf_prob(word0, cl_word_iv)
                word0 = cl_word_iv
            else:
                return ret
        # first word encountered, so let's reset hit scores first and then look for the hits
        self.cache_scores = []
        for doc_id, word_position in self.word_index[word0]:
            # prev_end_time = prev_tbeg + prev_dur
            prev_end_time = self.doc_index[doc_id][word_position][2]+self.doc_index[doc_id][word_position][3]
            hit = True # hit flag  
            for i in range(1, len(query_words)):
                # checking phrase in the document
                pointer_position = word_position + i
                # checking we are not exceeding array bounds and the time condition (1/2 second rule)
                if pointer_position >= len(self.doc_index[doc_id]) or self.doc_index[doc_id][pointer_position][2] - 0.5 > prev_end_time:
                    hit = False; break
                else:
                    # next word doc = next word phrase
                    if self.doc_index[doc_id][pointer_position][0] == query_words[i].lower():
                        # prev_end_time = prev_tbeg + prev_dur
                        prev_end_time = self.doc_index[doc_id][pointer_position][2] + self.doc_index[doc_id][pointer_position][3]
                    # if the queried word does NOT match, we check if it is an OOV word (only if we are using grapheme confusion matrix)
                    elif self.grapheme_mtx is not None and query_words[i].lower() not in self.word_index:
                        cl_query_word_iv = self._get_closest_word_iv(query_words[i].lower())
                        if self.doc_index[doc_id][pointer_position][0] == cl_query_word_iv:
                            prev_end_time = self.doc_index[doc_id][pointer_position][2] + self.doc_index[doc_id][pointer_position][3]
                            conf_prob *= self._calc_conf_prob(query_words[i].lower(), cl_query_word_iv)
                        else:
                            hit = False; break
                    else:
                        hit = False; break
            
            if hit:
                # word in doc
                ret_word = self.doc_index[doc_id][word_position][0]
                # channel
                ret_ch = self.doc_index[doc_id][word_position][1]
                # beginning time
                ret_tbeg = self.doc_index[doc_id][word_position][2]
                # total duration of phrase = last word beg_time + last word dur - first word beg_time
                ret_dur = self.doc_index[doc_id][word_position+len(query_words)-1][2] + \
                            self.doc_index[doc_id][word_position+len(query_words)-1][3] - ret_tbeg
                ret_dur = round(ret_dur, 2)
                # scores
                self._cache_scores(doc_id, word_position, len(query_words))
                # query hit information
                ret_item = (doc_id, ret_word, ret_ch, ret_tbeg, ret_dur) # ret_score will need to be appended afterwards
                ret.append(ret_item)
        
        ret = self._calculate_scores(ret, len(query_words), metric='prod', score_norm=score_norm, gamma=gamma)
        return ret



if __name__ == '__main__':
    if '-graph' in sys.argv:
        indexer = Indexer('./lib/kws/grapheme.map')
    else:
        indexer = Indexer()

    indexer.build_index('./lib/ctms/reference.ctm')

    print(indexer.search_query('nimwachie'))
    # expected output:
    #   file="BABEL_OP2_202_92740_20130923_235638_outLine" channel="1" tbeg="104.61" dur="0.75" score="1.000000"

    #print(indexer.search_query('what'))

    print(indexer.search_query('what she has gone'))
    # expected output:
    #   file="BABEL_OP2_202_29663_20131208_035816_outLine" channel="1" tbeg="217.41" dur="0.83" score="1.000000"

    print(indexer.search_query('what she has gonee'))
    # expected output IF USING GRAPHEME CONFUSION MATRIX:
    #   file="BABEL_OP2_202_29663_20131208_035816_outLine" channel="1" tbeg="217.41" dur="0.83" score="1.000000"
    # expected output IF *NOT* USING GRAPHEME CONFUSION MATRIX:
    #   []