import sys
from os import listdir


GDBMNT_FOLDER_PATH = "/../rds/project/rds-xyBFuSj0hm0/MLMI8.L2022/GDBNMT/"
WORDCLASS_FILE_PATH = GDBMNT_FOLDER_PATH + "wordclasses"
MAPPING_FILE_PATH = GDBMNT_FOLDER_PATH + "/fsts/w+l.map.de"

OUTPUT_FILE = "fsts/wtoc.txt"


def main():
    fout = open(OUTPUT_FILE, 'w')

    seen_words = set()

    # adding word to word and word to word_class    
    with open(WORDCLASS_FILE_PATH, 'r') as fin:
        for line in fin.readlines():
            word, word_class = line[:-1].split()

            # checkign if that word has been seen
            if word not in seen_words:
                # if not seen, add map word to itself
                fout.write("0\t0\t"+word+"\t"+word+"\n")
                seen_words.add(word)

            # add map word to word class
            fout.write("0\t0\t"+word+"\t"+word_class+"\n")
    
    # adding special symbols
    with open(MAPPING_FILE_PATH, 'r') as fin:
        for line in fin.readlines():
            symbol, _ = line[:-1].split()
            if ('.l.' in symbol) or (symbol in seen_words): 
                continue

            fout.write("0\t0\t"+symbol+"\t"+symbol+"\n")

    # specifying that 0 is the final state
    fout.write("0\n")

    fout.close()

'''
def main2():
    fout = open(OUTPUT_FILE, 'w')

    seen_words = set()

    # adding word to word and word to word_class    
    with open(MAP_FILE_PATH, 'r') as fin:
        for line in fin.readlines():
            word, word_class = line[:-1].split()

            # add map word to word class
            fout.write("0 0 "+word+" "+word_class+"\n")

            # checkign if that word has been seen
            if word not in seen_words:
                # if not seen, add map word to itself
                fout.write("0 0 "+word+" "+word+"\n")
                seen_words.add(word)
    
    # adding special characters
    fout.write("0 0 <epsilon> <epsilon>\n")
    fout.write("0 0 <s> <s>\n")
    fout.write("0 0 </s> </s>\n")
    fout.write("0 0 <unk> <unk>\n")

    fout.close()
'''


if __name__ == '__main__':
    main()