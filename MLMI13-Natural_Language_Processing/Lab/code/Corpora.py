import os, codecs, sys
from nltk.stem.porter import PorterStemmer

class MovieReviewCorpus():
    def __init__(self,stemming,pos):
        """
        initialisation of movie review corpus.

        @param stemming: use porter's stemming?
        @type stemming: boolean

        @param pos: use pos tagging?
        @type pos: boolean
        """
        # raw movie reviews
        self.reviews=[]
        # held-out train/test set
        self.train=[]
        self.test=[]
        # folds for cross-validation
        self.folds={}
        # porter stemmer
        self.stemmer=PorterStemmer() if stemming else None
        # part-of-speech tags
        self.pos=pos
        # import movie reviews
        self.get_reviews()


    def _read_datafolder(self, extension='txt', sign='POS'):
        DATA_PATH = "data/reviews/"
        data_path = DATA_PATH + sign + "/"

        all_files = os.listdir(data_path)

        for file in all_files:
            if file[-3:] == extension:
                with open(data_path+file, 'r') as f:
                    for line in f:
                        if len(line) > 1:
                            line_wo_final_period = line[:-2] # deliting \n and final period
                            review_tuple = (sign, line_wo_final_period.split())
                            #print(file, '-', review_tuple)
                            self.reviews.append(review_tuple)
                            
                            if file[:3] == 'cv9':
                                self.test.append(review_tuple)
                            else:
                                self.train.append(review_tuple)

                            fold_num = int(file[2])
                            if fold_num in self.folds:
                                self.folds[fold_num].append(review_tuple)
                            else:
                                self.folds[fold_num] = [review_tuple]




    def get_reviews(self):
        """
        processing of movie reviews.

        1. parse reviews in data/reviews and store in self.reviews.

           the format expected for reviews is: [(string,list), ...] e.g. [("POS",["a","good","movie"]), ("NEG",["a","bad","movie"])].
           in data/reviews there are .tag and .txt files. The .txt files contain the raw reviews and .tag files contain tokenized and pos-tagged reviews.

           to save effort, we recommend you use the .tag files. you can disregard the pos tags to begin with and include them later.
           when storing the pos tags, please use the format for each review: ("POS/NEG", [(token, pos-tag), ...]) e.g. [("POS",[("a","DT"), ("good","JJ"), ...])]

           to use the stemmer the command is: self.stemmer.stem(token)

        2. store training and held-out reviews in self.train/test. files beginning with cv9 go in self.test and others in self.train

        3. store reviews in self.folds. self.folds is a dictionary with the format: self.folds[fold_number] where fold_number is an int 0-9.
           you can get the fold number from the review file name.
        """
        # TODO Q0

        self._read_datafolder(extension='txt', sign='POS')
        self._read_datafolder(extension='txt', sign='NEG')

        print(self.reviews[0])
        print(self.folds[8][0])


        
        