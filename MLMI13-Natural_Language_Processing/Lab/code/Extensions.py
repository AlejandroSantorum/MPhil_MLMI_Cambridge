import numpy, os
from subprocess import call
from gensim.models import Doc2Vec
from sklearn import svm
from Classifiers import SVMText


class SVMDoc2Vec(SVMText):
    """ 
    class for baseline extension using SVM with Doc2Vec pre-trained vectors
    """
    def __init__(self,model):
        """
        initialisation of SVMDoc2Vec classifier.

        @param model: pre-trained doc2vec model to use
        @type model: string (e.g. random_model.model)

        @param svmlight_dir: location of local binaries for svmlight
        @type svmlight_dir: string
        """
        self.svm_classifier = svm.SVC()
        self.predictions = []
        self.model = model

    def normalize(self,vector):
        """
        normalise vector between -1 and 1 inclusive.

        @param vector: vector inferred from doc2vec
        @type vector: numpy array

        @return: normalised vector
        """
        # TODO Q8

    # since using pre-trained vectors don't need to determine features
    def getFeatures(self,reviews):
        """
        infer document vector for each review and add it to the list of features.
        @param reviews: movie reviews
        @type reviews: list of (string, list) tuples corresponding to (label, content)
        """

        self.input_features = []
        self.labels = []

        # TODO Q8
