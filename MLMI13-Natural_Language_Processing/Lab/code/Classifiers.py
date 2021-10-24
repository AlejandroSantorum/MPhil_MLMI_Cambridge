import os
from subprocess import call
from nltk.util import ngrams
from Analysis import Evaluation
import numpy as np
from sklearn import svm

class NaiveBayesText(Evaluation):
    def __init__(self,smoothing,bigrams,trigrams,discard_closed_class):
        """
        initialisation of NaiveBayesText classifier.

        @param smoothing: use smoothing?
        @type smoothing: booleanp

        @param bigrams: add bigrams?
        @type bigrams: boolean

        @param trigrams: add trigrams?
        @type trigrams: boolean

        @param discard_closed_class: restrict unigrams to nouns, adjectives, adverbs and verbs?
        @type discard_closed_class: boolean
        """
        # set of features for classifier
        self.vocabulary=set()
        # prior probability
        self.prior={}
        # conditional probablility
        self.condProb={}
        # use smoothing?
        self.smoothing=smoothing
        # add bigrams?
        self.bigrams=bigrams
        # add trigrams?
        self.trigrams=trigrams
        # restrict unigrams to nouns, adjectives, adverbs and verbs?
        self.discard_closed_class=discard_closed_class
        # stored predictions from test instances
        self.predictions=[]

    def extractVocabulary(self,reviews):
        """
        extract features from training data and store in self.vocabulary.

        @param reviews: movie reviews
        @type reviews: list of (string, list) tuples corresponding to (label, content)
        """
        for sentiment,review in reviews:
            for token in self.extractReviewTokens(review):
                self.vocabulary.add(token)

    def extractReviewTokens(self,review):
        """
        extract tokens from reviews.

        @param reviews: movie reviews
        @type reviews: list of (string, list) tuples corresponding to (label, content)

        @return: list of strings
        """
        text=[]
        for token in review:
            # check if pos tags are included in review e.g. ("bad","JJ")
            if len(token)==2 and self.discard_closed_class:
                if token[1][0:2] in ["NN","JJ","RB","VB"]: text.append(token)
            else:
                text.append(token)
        if self.bigrams:
            for bigram in ngrams(review,2): text.append(bigram)
        if self.trigrams:
            for trigram in ngrams(review,3): text.append(trigram)
        return text

    def create_vocab_dict(self):
        vocab_to_id = {}
        for word in self.vocabulary:
            vocab_to_id[word] = len(vocab_to_id)
        return vocab_to_id

    def train(self,reviews):
        """
        train NaiveBayesText classifier.

        1. reset self.vocabulary, self.prior and self.condProb
        2. extract vocabulary (i.e. get features for training)
        3. get prior and conditional probability for each label ("POS","NEG") and store in self.prior and self.condProb
           note: to get conditional concatenate all text from reviews in each class and calculate token frequencies
                 to speed this up simply do one run of the movie reviews and count token frequencies if the token is in the vocabulary,
                 then iterate the vocabulary and calculate conditional probability (i.e. don't read the movie reviews in their entirety
                 each time you need to calculate a probability for each token in the vocabulary)

        @param reviews: movie reviews
        @type reviews: list of (string, list) tuples corresponding to (label, content)
        """
        # TODO Q1
        self.extractVocabulary(reviews)
        
        total_pos_reviews = 0
        total_neg_reviews = 0
        self.condProb["POS"] = {}
        self.condProb["NEG"] = {}

        for sentiment,review in reviews:
            if sentiment == "POS":
                # calculating total number of positive reviews
                total_pos_reviews += 1
                # calculating appearences for conditional probabilities
                for token in review:
                    if token in self.vocabulary:
                        if token in self.condProb["POS"]:
                            self.condProb["POS"][token] += 1
                        else:
                            self.condProb["POS"][token] = 1

            else:
                # calculating total number of negative reviews
                total_neg_reviews += 1
                # calculating appearences for conditional probabilities
                for token in review:
                    if token in self.vocabulary:
                        if token in self.condProb["NEG"]:
                            self.condProb["NEG"][token] += 1
                        else:
                            self.condProb["NEG"][token] = 1

        # calculating priors
        self.prior["POS"] = total_pos_reviews/len(reviews)
        self.prior["NEG"] = total_neg_reviews/len(reviews)

        # calculating conditional probabilities by calculating frequencies per class
        total_words_in_pos = sum(self.condProb["POS"].values())
        total_words_in_neg = sum(self.condProb["NEG"].values())
        for token in self.vocabulary:
            if token in self.condProb["POS"]:
                self.condProb["POS"][token] /= total_words_in_pos
            if token in self.condProb["NEG"]:
                self.condProb["NEG"][token] /= total_words_in_neg

        # TODO Q2 (use switch for smoothing from self.smoothing)


    def test(self,reviews):
        """
        test NaiveBayesText classifier and store predictions in self.predictions.
        self.predictions should contain a "+" if prediction was correct and "-" otherwise.

        @param reviews: movie reviews
        @type reviews: list of (string, list) tuples corresponding to (label, content)
        """
        # TODO Q1
        for sentiment,review in reviews:
            arg_pos = np.log(self.prior["POS"])
            arg_neg = np.log(self.prior["NEG"])

            for token in review:
                if token in self.vocabulary:
                    if token in self.condProb["POS"]:
                        arg_pos += np.log(self.condProb["POS"][token])
                    if token in self.condProb["NEG"]:
                        arg_neg += np.log(self.condProb["NEG"][token])

            '''
            print("Review:", review)
            print("Sentiment:", sentiment)
            print("Arg POS:", arg_pos)
            print("Arg NEG:", arg_neg)
            '''

            if arg_pos > arg_neg and sentiment == "POS":
                self.predictions.append("+")
            elif arg_pos < arg_neg and sentiment == "NEG":
                self.predictions.append("-")
            elif arg_pos == arg_neg:
                # If posterior is equal for both classes, then we choose the class with highest prior
                if self.prior["POS"] > self.prior["NEG"] and sentiment == "POS":
                    self.predictions.append("+")
                elif self.prior["POS"] < self.prior["NEG"] and sentiment == "NEG":
                    self.predictions.append("+")
                else:
                    self.predictions.append("-")
            else:
                self.predictions.append("-")








class SVMText(Evaluation):
    def __init__(self,bigrams,trigrams,discard_closed_class):
        """
        initialisation of SVMText object

        @param bigrams: add bigrams?
        @type bigrams: boolean

        @param trigrams: add trigrams?
        @type trigrams: boolean

        @param svmlight_dir: location of smvlight binaries
        @type svmlight_dir: string

        @param svmlight_dir: location of smvlight binaries
        @type svmlight_dir: string

        @param discard_closed_class: restrict unigrams to nouns, adjectives, adverbs and verbs?
        @type discard_closed_class: boolean
        """
        self.svm_classifier = svm.SVC()
        self.predictions=[]
        self.vocabulary=set()
        # add in bigrams?
        self.bigrams=bigrams
        # add in trigrams?
        self.trigrams=trigrams
        # restrict to nouns, adjectives, adverbs and verbs?
        self.discard_closed_class=discard_closed_class

    def extractVocabulary(self,reviews):
        self.vocabulary = set()
        for sentiment, review in reviews:
            for token in self.extractReviewTokens(review):
                 self.vocabulary.add(token)

    def extractReviewTokens(self,review):
        """
        extract tokens from reviews.

        @param reviews: movie reviews
        @type reviews: list of (string, list) tuples corresponding to (label, content)

        @return: list of strings
        """
        text=[]
        for term in review:
            # check if pos tags are included in review e.g. ("bad","JJ")
            if len(term)==2 and self.discard_closed_class:
                if term[1][0:2] in ["NN","JJ","RB","VB"]: text.append(term)
            else:
                text.append(term)
        if self.bigrams:
            for bigram in ngrams(review,2): text.append(term)
        if self.trigrams:
            for trigram in ngrams(review,3): text.append(term)
        return text

    def getFeatures(self,reviews):
        """
        determine features and labels from training reviews.

        1. extract vocabulary (i.e. get features for training)
        2. extract features for each review as well as saving the sentiment
        3. append each feature to self.input_features and each label to self.labels
        
        @param reviews: movie reviews
        @type reviews: list of (string, list) tuples corresponding to (label, content)
        """

        self.input_features = []
        self.labels = []

        # TODO Q6.

    def train(self,reviews):
        """
        train svm

        @param reviews: training data
        @type reviews: list of (string, list) tuples corresponding to (label, content)
        """
        # function to determine features in training set.
        self.getFeatures(reviews)

        # train SVM model
        self.svm_classifier.fit(self.input_features, self.labels)

    def test(self,reviews):
        """
        test svm

        @param reviews: test data
        @type reviews: list of (string, list) tuples corresponding to (label, content)
        """

        # TODO Q6.1
