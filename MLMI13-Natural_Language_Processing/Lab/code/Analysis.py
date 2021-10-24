import math,sys

class Evaluation():
    """
    general evaluation class implemented by classifiers
    """
    def crossValidate(self,corpus):
        """
        function to perform 10-fold cross-validation for a classifier.
        each classifier will be inheriting from the evaluation class so you will have access
        to the classifier's train and test functions.

        1. read reviews from corpus.folds and store 9 folds in train_files and 1 in test_files
        2. pass data to self.train and self.test e.g., self.train(train_files)
        3. repeat for another 9 runs making sure to test on a different fold each time

        @param corpus: corpus of movie reviews
        @type corpus: MovieReviewCorpus object
        """
        # reset predictions
        self.predictions=[]

        # TODO Q3
        all_fold_predictions = []
        n_folds = len(corpus.folds)
        for i in range(n_folds):
            # test fold
            test_reviews = corpus.folds[i]
            # building train set using the rest of the folds
            train_reviews = []
            for j in range(n_folds):
                if i != j:
                    train_reviews += corpus.folds[j]
            
            self.train(train_reviews)
            self.test(test_reviews)
            all_fold_predictions += self.predictions

        self.predictions = all_fold_predictions
            

    def getStdDeviation(self):
        """
        get standard deviation across folds in cross-validation.
        """
        # get the avg accuracy and initialize square deviations
        avgAccuracy,square_deviations=self.getAccuracy(),0
        # find the number of instances in each fold
        fold_size=len(self.predictions)//10
        # calculate the sum of the square deviations from mean
        for fold in range(0,len(self.predictions),fold_size):
            square_deviations+=(self.predictions[fold:fold+fold_size].count("+")/float(fold_size) - avgAccuracy)**2
        # std deviation is the square root of the variance (mean of square deviations)
        return math.sqrt(square_deviations/10.0)

    def getAccuracy(self):
        """
        get accuracy of classifier.

        @return: float containing percentage correct
        """
        # note: data set is balanced so just taking number of correctly classified over total
        # "+" = correctly classified and "-" = error
        return self.predictions.count("+")/float(len(self.predictions))
