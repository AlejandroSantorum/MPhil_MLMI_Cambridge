import numpy, os
from subprocess import call
from gensim.models import Doc2Vec
from gensim.test.utils import get_tmpfile
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
    def getFeatures(self,reviews_embeddings):
        """
        infer document vector for each review and add it to the list of features.
        @param reviews: movie reviews
        @type reviews: list of (string, list) tuples corresponding to (label, content)
        """

        self.input_features = []
        self.labels = []

        # TODO Q8

    def train(self, train_embeddings, train_labels):
        self.svm_classifier.fit(train_embeddings, train_labels)

    def test(self, test_embeddings, test_labels):
        pred_labels = self.svm_classifier.predict(test_embeddings)

        n_labels = len(test_labels)
        for i in range(n_labels):
            if test_labels[i] == pred_labels[i]:
                self.predictions.append("+")
            else:
                self.predictions.append("-")
