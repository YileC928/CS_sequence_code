"""
CS121: Analyzing Election Tweets (Solutions)

Algorithms for efficiently counting and sorting distinct `entities`,
or unique values, are widely used in data analysis.

Functions to implement:

- count_tokens
- find_top_k
- find_min_count
- find_most_salient

You may add helper functions.
"""

import math
from util import sort_count_pairs

####1.1
def count_tokens(tokens):
    '''
    Counts each distinct token (entity) in a list of tokens

    Inputs:
        tokens: list of tokens (must be immutable)

    Returns: dictionary that maps tokens to counts
    '''
    count_d = {}
    tokens_no_rep = []
    for i in tokens:
        if i not in tokens_no_rep:
            tokens_no_rep.append(i)

    for j in tokens_no_rep:
        count_d[j] = 0
        for i in tokens:
            if j == i:
                count_d[j] += 1

    return count_d


####1.2
def find_top_k(tokens, k):
    '''
    Find the k most frequently occuring tokens

    Inputs:
        tokens: list of tokens (must be immutable)
        k: a non-negative integer

    Returns: list of the top k tokens ordered by count.
    '''
    if k < 0:
        raise ValueError("In find_top_k, k must be a non-negative integer")

    #Count tokens
    d_count = count_tokens(tokens)
    #Convert dict in to list of tuples
    lst_pairs = []
    for key, value in d_count.items():
        pair = (key, value)
        lst_pairs.append(pair)
    #Sort by count
    sorted_lst = sort_count_pairs(lst_pairs)
    #Extract the K tokens
    lst_top_k = []
    for pair in sorted_lst[0:k]:
        lst_top_k.append(pair[0])

    return lst_top_k


####1.3
def find_min_count(tokens, min_count):
    '''
    Find the tokens that occur *at least* min_count times

    Inputs:
        tokens: a list of tokens  (must be immutable)
        min_count: a non-negative integer

    Returns: set of tokens
    '''
    if min_count < 0:
        raise ValueError("min_count must be a non-negative integer")

    d_count = count_tokens(tokens)
    lst_above_min = []

    for k, v in d_count.items():
        if v >= min_count:
            lst_above_min.append(k)

    return set(lst_above_min)


####1.4
def find_tf (doc):
    '''
    Compute tf for one document.

    Inputs:
      doc: list of tokens

    Returns: dictionary mapping tfs to tokens
    '''
    if doc == []:
        dict_tf = {}
    else:
        doc_count = count_tokens(doc)
        max_t = find_top_k(doc, 1)[0]
        num_max_t = doc_count[max_t]

        dict_tf = {}
        for k, v in doc_count.items():
            tf = 0.5 + 0.5 * (v/num_max_t)
            dict_tf[k] = tf

    return dict_tf

def find_idf(docs):
    '''
    Compute idf for each document.

    Inputs:
      docs: list of list of tokens

    Returns: dictionary mapping tfs to tokens
    '''
    num_docs = len(docs)
    dict_idf = {}

    #generate a list of non-repetitive tokens
    lst_t = []
    for doc in docs:
        for t in doc:
            if t not in lst_t:
                lst_t.append(t)

    #calculate idf for each token in the non-repetitive list
    for t1 in lst_t:
        num_occur_t1 = 0
        for doc in docs:
            if t1 in doc:
                num_occur_t1 += 1
        dict_idf[t1] = math.log(num_docs/num_occur_t1)

    return dict_idf


def find_salient(docs, threshold):
    '''
    Compute the salient words for each document.  A word is salient if
    its tf-idf score is strictly above a given threshold.

    Inputs:
      docs: list of list of tokens
      threshold: float

    Returns: list of sets of salient words
    '''
    dict_idf = find_idf(docs)
    lst_sa_tokens = []

    for doc in docs:
        dict_tf = find_tf(doc)
        tf_idf = {}
        for k, v in dict_tf.items():
            tf_idf[k] = v * dict_idf[k]

        sa_tokens = []
        for k1 in tf_idf:
            if tf_idf[k1] > threshold:
                sa_tokens.append(k1)

        lst_sa_tokens.append(set(sa_tokens))

    return lst_sa_tokens
