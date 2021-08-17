"""
Analyze module
"""

import unicodedata
import sys

from basic_algorithms import find_top_k, find_min_count, find_salient

##################### DO NOT MODIFY THIS CODE #####################

def keep_chr(ch):
    '''
    Find all characters that are classifed as punctuation in Unicode
    (except #, @, &) and combine them into a single string.
    '''
    return unicodedata.category(ch).startswith('P') and \
        (ch not in ("#", "@", "&"))

PUNCTUATION = " ".join([chr(i) for i in range(sys.maxunicode)
                        if keep_chr(chr(i))])

# When processing tweets, ignore these words
STOP_WORDS = ["a", "an", "the", "this", "that", "of", "for", "or",
              "and", "on", "to", "be", "if", "we", "you", "in", "is",
              "at", "it", "rt", "mt", "with"]

# When processing tweets, words w/ a prefix that appears in this list
# should be ignored.
STOP_PREFIXES = ("@", "#", "http", "&amp")


#####################  MODIFY THIS CODE #####################


############## Part 2 ##############

def generate_lst_entities (tweets, entity_desc):
    '''
    Generate a lst of entities from tweets

    Inputs:
        tweets: a list of tweets
        entity_desc: a triple ("hashtags", "text", True),
          ("user_mentions", "screen_name", False), etc

    Returns: list of entities
    '''
    lst_entities = []

    entity_type, entity_info, case_sen = entity_desc
    for tweet in tweets:
        for entity_d in tweet["entities"][entity_type]:
            if not case_sen:
                entity = entity_d[entity_info].lower()
            else:
                entity = entity_d[entity_info]
            lst_entities.append(entity)

    return lst_entities

#Task 2.1
def find_top_k_entities(tweets, entity_desc, k):
    '''
    Find the k most frequently occuring entitites

    Inputs:
        tweets: a list of tweets
        entity_desc: a triple ("hashtags", "text", True),
          ("user_mentions", "screen_name", False), etc
        k: integer

    Returns: list of entities
    '''
    lst_top_k = []
    lst_entities = generate_lst_entities (tweets, entity_desc)
    lst_top_k = find_top_k(lst_entities, k)

    return lst_top_k

#Task 2.2
def find_min_count_entities(tweets, entity_desc, min_count):
    '''
    Find the entitites that occur at least min_count times.

    Inputs:
        tweets: a list of tweets
        entity_desc: a triple ("hashtags", "text", True),
          ("user_mentions", "screen_name", False), etc
        min_count: integer

    Returns: set of entities
    '''
    lst_min_count = []
    lst_entities = generate_lst_entities (tweets, entity_desc)

    lst_min_count = find_min_count(lst_entities, min_count)

    return lst_min_count



############## Part 3 ##############
def pre_process(tweets, case_se):
    '''
    Preprocess the tweets

    Inputs:
        tweets: a list of tweets
        case_se: boolean

    Returns: list of cleaned tweets
    '''
    lst_ab_text_cleaned = []
    for tweet in tweets:
        ab_text = tweet["abridged_text"]
        ab_text = ab_text.split()
        ab_text_cleaned = []
        for i in ab_text:
            i = i.strip (PUNCTUATION)
            if (not i.startswith(STOP_PREFIXES)) and (i not in PUNCTUATION):
                if case_se:
                    if i not in STOP_WORDS:
                        ab_text_cleaned.append(i)
                else:
                    ab_text_cleaned.append(i.lower())

        lst_ab_text_cleaned.append(ab_text_cleaned)

    return lst_ab_text_cleaned

def rep_n_grams (tweets, n, case_se):
    '''
    Represent n grams

    Inputs:
        tweets: a list of tweets
        n: integer
        case_se: boolean

    Returns: list of n-grams
    '''
    lst_text_cleaned = pre_process(tweets, case_se)
    lst_grams = []

    for text in lst_text_cleaned:
        for i in range(len(text) - (n-1)):
            lst_gram = []
            for j in range(i, i+n):
                lst_gram.append(text[j])
            lst_grams.append(tuple(lst_gram))

    return lst_grams

#Task.3.1
def find_top_k_ngrams(tweets, n, case_sensitive, k):
    '''
    Find k most frequently occurring n-grams

    Inputs:
        tweets: a list of tweets
        n: integer
        case_sensitive: boolean
        k: integer

    Returns: list of n-grams
    '''
    tweets_as_grams = rep_n_grams (tweets, n, case_sensitive)
    top_k_ngrams = find_top_k(tweets_as_grams, k)

    return top_k_ngrams

#Task3.2
def find_min_count_ngrams(tweets, n, case_sensitive, min_count):
    '''
    Find n-grams that occur at least min_count times.

    Inputs:
        tweets: a list of tweets
        n: integer
        case_sensitive: boolean
        min_count: integer

    Returns: set of n-grams
    '''
    tweets_as_grams = rep_n_grams (tweets, n, case_sensitive)
    min_count_ngrams = find_min_count(tweets_as_grams, min_count)

    return min_count_ngrams

#Task3.3
def pre_process_33(tweets, case_se):
    '''
    Preprocess the tweets for task3.3

    Inputs:
        tweets: a list of tweets
        case_se: boolean

    Returns: list of cleaned tweets
    '''
    lst_ab_text_cleaned = []
    for tweet in tweets:
        ab_text = tweet["abridged_text"]
        ab_text = ab_text.split()
        ab_text_cleaned = []

        for i in ab_text:
            i = i.strip (PUNCTUATION)
            if (not i.startswith(STOP_PREFIXES)) and (i not in PUNCTUATION):
                if case_se:
                    ab_text_cleaned.append(i)
                else:
                    ab_text_cleaned.append(i.lower())

        lst_ab_text_cleaned.append(ab_text_cleaned)

    return lst_ab_text_cleaned

def rep_n_grams_33 (tweets, n, case_se):
    '''
    Represent n grams for task3.3

    Inputs:
        tweets: a list of tweets
        n: integer
        case_se: boolean

    Returns: list of n-grams
    '''
    lst_text_cleaned = pre_process_33(tweets, case_se)
    lst_grams_tot = []

    for text in lst_text_cleaned:
        lst_grams = []
        for i in range(len(text) - (n-1)):
            lst_gram = []
            for j in range(i, i+n):
                lst_gram.append(text[j])
            lst_grams.append(tuple(lst_gram))
        lst_grams_tot.append(lst_grams)
    return lst_grams_tot

def find_salient_ngrams(tweets, n, case_sensitive, threshold):
    '''
    Find the salient n-grams for each tweet.

    Inputs:
        tweets: a list of tweets
        n: integer
        case_sensitive: boolean
        threshold: float

    Returns: list of sets of strings
    '''

    tweets_as_grams = rep_n_grams_33(tweets, n, case_sensitive)
    print(tweets_as_grams)
    salient_ngrams = find_salient(tweets_as_grams, threshold)

    return salient_ngrams
