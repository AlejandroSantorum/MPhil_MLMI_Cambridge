from sampleDiscrete import sampleDiscrete
import scipy.io as sio
import numpy as np


def BMM(A, B, K, alpha, gamma):

    """

    :param A: Training data [D, 3]
    :param B: Test Data [D, 3]
    :param K: number of mixture components
    :param alpha: parameter of the Dirichlet over mixture components
    :param gamma: parameter of the Dirichlet over words
    :return: test perplexity and multinomial weights over words
    """
    W = np.max([np.max(A[:, 1]), np.max(B[:, 1])])  # total number of unique words
    D = np.max(A[:, 0])  # number of documents in A

    # Initialization: assign each document a mixture component at random
    sd = np.floor(K * np.random.rand(D)).astype(int)   # mixture component assignment
    swk = np.zeros((W, K))  # K multinomials over W unique words
    sk_docs = np.zeros((K, 1), dtype=int)  # number of documents assigned to each mixture
    # Populate the count matrices by looping over documents
    for d in range(D):
        training_documents = np.where(A[:, 0] == d+1)  # get all occurrences of document d in the training data
        w = np.array(A[training_documents, 1])  # number of unique words in document d
        c = np.array(A[training_documents, 2])  # counts of words in document d
        k = sd[d]  # document d is in mixture k
        swk[w-1, k] += c  # number of times w is assigned to component k
        sk_docs[k] += 1

    sk_words = np.sum(swk, axis=0)  # number of words assigned to mixture k over all docs

    num_iters_gibbs = 10
    # Perform Gibbs sampling through all documents and words
    for iter in range(num_iters_gibbs):
        for d in range(D):

            training_documents = np.where(A[:, 0] == d+1)  # get all occurrences of document d in trh training data
            w = A[training_documents, 1]  # number of unique words in document d
            c = A[training_documents, 2]  # counts of words in document d
            old_class = sd[d]  # document d is in mixture k
            # remove document from counts
            swk[w-1, old_class] -= c  # decrease number of times w is assigned to component k
            sk_docs[old_class] -= 1  # remove document d from count of docs
            sk_words[old_class] -= np.sum(c)  # remove word counts from mixture
            # resample class of document
            lb = np.zeros(K)  # log probability of doc d under mixture component k

            for k in range(K):
                ll = np.dot(np.log(swk[w-1, k] + gamma) - np.log(sk_words[k] + gamma * W), c.T)

                lb[k] = np.log(sk_docs[k] + alpha) + ll
            b = np.exp(lb - np.max(lb))  # exponentiation of log probability plus constant
            kk = sampleDiscrete(b, np.random.rand())  # sample from (un-normalized) multinomial distribution
            # update counts based on new class assignment
            swk[w-1, kk] += c  # number of times w is assigned to component k
            sk_docs[kk] += 1
            sk_words[kk] += np.sum(c)
            sd[d] = kk

    # test documents
    lp = 0
    nd = 0
    unique_docs_in_b = np.unique(B[:, 0])
    for doc in unique_docs_in_b:
        test_docs = np.where(B[:, 0] == doc)
        w = B[test_docs, 1]  # unique words in doc d
        c = B[test_docs, 2]  # counts
        z = np.log(sk_docs + alpha) - np.log(np.sum(sk_docs + alpha))
        for k in range(K):
            b = (swk[:, k] + gamma) / (sk_words[k] + gamma * W)
            z[k] += np.dot(c, np.log(b[w-1]).T)[0]  # probability for doc d
        lp += np.log(np.sum(np.exp(z - np.max(z)))) + np.max(z)  # log-sum-exp to compute normalization constant
        nd += np.sum(c)

    perplexity = np.exp(-lp/nd)  # perplexity

    return perplexity, swk

if __name__ == '__main__':
    np.random.seed(1)
    # load data
    data = sio.loadmat('kos_doc_data.mat')
    A = np.array(data['A'])
    B = data['B']
    V = data['V']
    K = 20  # number of clusters
    alpha = 10  # parameter of the Dirichlet over mixture components
    gamma = .1  # parameter of the Dirichlet over words
    perplexity, swk = BMM(A, B, K, alpha, gamma)
    print(perplexity)
    I = 20
    indices = np.argsort(-swk, axis=0)
    indices = indices[:20, :]
    top_words = V[indices]
    for topic in top_words[:, :, 0].T:
        print('\n')
        for word in topic:
            print(word[0])



