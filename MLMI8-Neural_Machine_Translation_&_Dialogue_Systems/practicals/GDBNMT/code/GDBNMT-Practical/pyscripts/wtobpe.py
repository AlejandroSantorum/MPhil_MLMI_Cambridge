import sys


GDBMNT_FOLDER_PATH = "/../rds/project/rds-xyBFuSj0hm0/MLMI8.L2022/GDBNMT/"
# special characters mapping
SCMAP_FILE_PATH = GDBMNT_FOLDER_PATH + "/fsts/w+l.map.de"
# word to subword mapping
SUBWMAP_FILE_PATH = GDBMNT_FOLDER_PATH + "/fairseq.pretrained/word_bpe.dict"

OUTPUT_FILE = "fsts/wtobpe.txt"


def main():
    fout = open(OUTPUT_FILE, 'w')

    seen_words = set()

    # word to subword    
    with open(SUBWMAP_FILE_PATH, 'r') as fin:
        next_state = 1
        for line in fin.readlines():
            tokens = line[:-1].split()
            word = tokens[0]
            seen_words.add(word)
            subword_seq = tokens[1:]
            # if the subword sequence is of length 1, then just create an ordinary loop from state 0 to 0
            if len(subword_seq) == 1:
                fout.write("0\t0\t"+word+"\t"+subword_seq[0]+"\n")
            else:
                # else, divide the sequence in first link (from 0 to next state),
                #   sequence of subwords (state to tate+1), and last link from
                #   last state to 0 again.         
                fout.write("0\t"+str(next_state)+"\t"+word+"\t"+subword_seq[0]+"\n")
                for subword in subword_seq[1:-1]:
                    fout.write(str(next_state)+"\t"+str(next_state+1)+"\t<epsilon>\t"+subword+"\n")
                    next_state += 1
                fout.write(str(next_state)+"\t0\t<epsilon>\t"+subword_seq[-1]+"\n")
                next_state += 1

    # adding special symbols
    with open(SCMAP_FILE_PATH, 'r') as fin:
        for line in fin.readlines():
            symbol, _ = line[:-1].split()
            if ('.l.' in symbol) or (symbol in seen_words): 
                continue

            fout.write("0\t0\t"+symbol+"\t"+symbol+"\n")

    # specifying that 0 is the final state
    fout.write("0\n")

    fout.close()



if __name__ == '__main__':
    main()