import numpy as np
from Levenshtein import distance as levenshtein_distance
from difflib import SequenceMatcher


def grapheme_to_idx(grapheme):
    if grapheme == 'sil' or grapheme == ' ':
        return -1
    if not grapheme.isalpha():
        return 0

    return ord(grapheme) - ord('a')


def build_grapheme_confusion_mtx(grapheme_file):
    grapheme_mtx = np.zeros((27,27)) # 26 letters in english alphabet + silence

    with open(grapheme_file, 'r') as f:
        for line in f.readlines():
            gra1, gra2, occ = line[:-1].split()
            idx1 = grapheme_to_idx(gra1)
            idx2 = grapheme_to_idx(gra2)
            grapheme_mtx[idx1][idx2] = occ
    
    # P(IV|OVV) = P(predicted|reference):
    #   because IV word (dict) is considered 'predicted' and OVV word (query) is considered 'reference'
    grapheme_mtx = np.transpose(grapheme_mtx)

    # normalising grapheme matrix => probabilities => columns must sum to 1
    sums_of_cols = np.sum(grapheme_mtx, axis=0)
    grapheme_mtx = grapheme_mtx / sums_of_cols
    return grapheme_mtx



if __name__ == '__main__':
    mtx = build_grapheme_confusion_mtx('./lib/kws/grapheme.map')
    print(np.sum(mtx, axis=0))

    # print(levenshtein_distance("abandoned", "  abandon"))

    # string1 = "qweabandonedrr"
    # string2 = "qabandoned"
    # (id1, id2, length) = SequenceMatcher(None, string1, string2).find_longest_match(0, len(string1), 0, len(string2))
    # print((id1, id2, length))
    # print(string1[id1: id1+length])
    # print(string2[id2: id2+length])