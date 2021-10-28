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

    
    def _read_txtfile(self, data_path, filename, sign):
        '''
            ¿¿¿ TODO ???
        '''
        pass


    def _read_tagfile(self, data_path, filename, sign):
        with open(data_path+filename, 'r') as f:
            review_list = []
            for line in f:
                # omitting empty lines
                if len(line) > 1:
                    # line[:-1] to delete final \n, and then splitting by tabs
                    word_tag_list = line[:-1].split("\t")
                    # stemming if specified at class constructor
                    if self.stemmer:
                        word_tag_list[0] = self.stemmer.stem(word_tag_list[0])
                    if self.pos:
                        word_tag = tuple(word_tag_list)
                        # adding (word, tag) to list
                        review_list.append(word_tag)
                    else:
                        # adding just the word to list
                        review_list.append(word_tag_list[0])

            # adding review
            review = (sign, review_list)
            self.reviews.append(review)

            # adding review to train/test sets
            if filename[:3] == 'cv9':
                self.test.append(review)
            else:
                self.train.append(review)

            # adding review to its corresponding fold
            fold_num = int(filename[4])
            if fold_num in self.folds:
                self.folds[fold_num].append(review)
            else:
                self.folds[fold_num] = [review]


    def _read_datafolder(self, extension='tag', sign='POS'):
        DATA_PATH = "data/reviews/"
        data_path = DATA_PATH + sign + "/"

        all_files = os.listdir(data_path)

        if extension == 'tag':
            for filename in all_files:
                if filename[-3:] == extension:
                    self._read_tagfile(data_path, filename, sign)

        elif extension == 'txt':
            for filename in all_files:
                if filename[-3:] == extension:
                    self._read_txtfile(data_path, filename)

        else:
            print("Corpora Error: given extension not suppported")


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

        self._read_datafolder(extension='tag', sign='POS')
        self._read_datafolder(extension='tag', sign='NEG')


        
        