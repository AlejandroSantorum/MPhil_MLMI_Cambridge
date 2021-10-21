import numpy, os
from subprocess import call
from gensim.models import Doc2Vec
from Classifiers import SVMText


class SVMDoc2Vec(SVMText):
    """ 
    class for baseline extension using SVM with Doc2Vec pre-trained vectors
    """
    def __init__(self,model,svmlight_dir):
        """
        initialisation of parent SVM object and self.model attribute
        to initialise SVM parent use: SVM.__init_(self,svmlight_dir)

        @param model: pre-trained doc2vec model to use
        @type model: string (e.g. random_model.model)

        @param svmlight_dir: location of local binaries for svmlight
        @type svmlight_dir: string
        """
        # TODO Q8

    def normalize(self,vector):
        """
        normalise vector between -1 and 1 inclusive.

        @param vector: vector inferred from doc2vec
        @type vector: numpy array

        @return: normalised vector
        """
        # TODO Q8

    def getVectors(self,reviews):
        """
        infer document vector for each review. 

        @param reviews: movie reviews
        @type reviews: list of (string, list) tuples corresponding to (label, content)

        @return: list of (string, list) tuples where string is the label ("1"/"-1") and list
                 contains the features in svmlight format e.g. ("1",[(1, 0.04), (2, 4.0), ...])
                 svmlight feature format is: (id, value) and id must be > 0.
        """
        # TODO Q8

    # since using pre-trained vectors don't need to determine features 
    def getFeatures(self,reviews):
        pass
