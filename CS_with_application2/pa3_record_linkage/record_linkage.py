'''
Linking restaurant records in Zagat and Fodor's list using restaurant
names, cities, and street addresses.

Yile Chen
'''

import csv
import jellyfish
import pandas as pd
import util

def find_matches(output_filename, mu, lambda_, block_on_city=False):
    '''
    Put it all together: read the data and apply the record linkage
    algorithm to classify the potential matches.

    Inputs:
      output_filename (string): the name of the output file,
      mu (float) : the maximum false positive rate,
      lambda_ (float): the maximum false negative rate,
      block_on_city (boolean): indicates whether to block on the city or not.
    '''

    zagat_filename = "data/zagat.csv"
    fodors_filename = "data/fodors.csv"
    known_links_filename = "data/known_links.csv"
    unmatch_pairs_filename = "data/unmatch_pairs.csv"
    df_zagat = pd.read_csv(zagat_filename, index_col = "index")
    df_fodors = pd.read_csv(fodors_filename, index_col = "index")
    df_know_links = pd.read_csv(known_links_filename, header = None)
    df_unmatch_pairs = pd.read_csv(unmatch_pairs_filename, header = None)
    
    categories = ["high", "medium", "low"]
    cat_lst = get_all_cat(categories)
    
    dct_prob_m = get_dct_prob(df_know_links, df_zagat, df_fodors, cat_lst)
    dct_prob_u = get_dct_prob(df_unmatch_pairs, df_zagat, df_fodors, cat_lst)
    lst_prob_tuple = get_lst_prob_tuple(dct_prob_m, dct_prob_u)
    dct_cat_class = get_cat_to_class(lst_prob_tuple, mu, lambda_, cat_lst)
    
    output_lst = []
    for i1 in range(df_zagat.shape[0]):
        for i2 in range(df_fodors.shape[0]):
            if not block_on_city:
                cat_tuple = get_cat_tuple(i1, i2, df_zagat, df_fodors)
                output_lst.append([i1, i2, dct_cat_class[cat_tuple]])
            else:
                if df_zagat.loc[i1].city == df_fodors.loc[i2].city:
                    cat_tuple = get_cat_tuple(i1, i2, df_zagat, df_fodors)
                    output_lst.append([i1, i2, dct_cat_class[cat_tuple]])
    
    with open(output_filename, 'w') as csvfile:  
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(output_lst)

### AUXILIARY FUNCTIONS
def jw_dist(string1, string2):
    '''
    generate jaro_winkler distance.
    Inputs:
      string1 (string): a string of interest,
      string2 (string): another string of interest.
    Outputs:
      jaro_winkler_similarity (float): the jaro_winkler
        disctance of the two  strings.
    '''
    return jellyfish.jaro_winkler_similarity(string1, string2)


def get_all_cat(categories):
    '''
    find the list of all category tuples.
    Inputs:
      categories (list): a list of categories - low, medium and high.
    Outputs:
      cat_lst (list): the list of all category tuples (in this pa, 27).
    '''
    cat_lst = []
    for cat1 in categories:
        for cat2 in categories:
            for cat3 in categories:
                cat_lst.append((cat1, cat2, cat3))
    return cat_lst

def get_cat_tuple(i, j, df_zagat, df_fodors):
    '''
    get category tuples for pairs of resteruant records.
    Inputs:
      i (int): index of a resteruant in zagat,
      j (int): index of another resteruant in fodor,
      df_zagat (dataframe): dataframe of the zagat data,
      df_fodor (dataframe): dataframe of the fodor data.
    Outputs:
      cat_tuple (list): list of category tuples (e.g.,
        ("high", "low", "medium")) of the pairs.
    '''
    res_z = df_zagat.loc[i, "restaurant name"]
    res_f = df_fodors.loc[j, "restaurant name"]
    jw_res = jw_dist(res_z, res_f)
    city_z = df_zagat.loc[i, "city"]
    city_f = df_fodors.loc[j, "city"]
    jw_city = jw_dist(city_z, city_f)
    add_z = df_zagat.loc[i, "street address"]
    add_f = df_fodors.loc[j, "street address"]
    jw_add = jw_dist(add_z, add_f)
    cat_tuple = (util.get_jw_category(jw_res),
                 util.get_jw_category(jw_city), util.get_jw_category(jw_add))
    return cat_tuple

def get_dct_prob(df, df_zagat, df_fodors, cat_lst):
    '''
    get a dictionary mapping category tuples to probabilities.
    Inputs:
      df (dataframe): a dataframe containing index pairs,
      df_zagat (dataframe): dataframe of the zagat data,
      df_fodor (dataframe): dataframe of the fodor data,
      cat_lst (list): list of all category tuples (in this pa, 27).
    Outputs:
      prob_dct (dict): a dictionary mapping category tuples to probabilities,
        e.g.{("high", "low", "medium"): 0}.
    '''
    prob_dct = dict.fromkeys(cat_lst, 0)
    for index in range(df.shape[0]):
        i, j = df.iloc[index]
        cat_tuple = get_cat_tuple(i, j, df_zagat, df_fodors)
        prob_dct[cat_tuple] += 1/df.shape[0]

    return prob_dct


def get_lst_prob_tuple(dct_prob_m, dct_prob_u):
    '''
    get a list of sorted tuples of three elements - category tuple, 
    match probability, and unmatch probability.
    Inputs:
      dct_prob_m (dict): dictionary mapping category tuples to match probabilities,
      dct_prob_u (dict): dictionary mapping category tuples to unmatch probabilities.
    Outputs:
      lst_prob_tuple (list): a list of tuples of three elements - category tuple,
        match probability, and unmatch probability.
    '''
    lst_prob_tuple = []
    for cat, prob_m in dct_prob_m.items():
        prob_u = dct_prob_u[cat]
        if not (prob_m == 0.0 and prob_u == 0.0):
            prob_tuple = (cat, prob_m, dct_prob_u[cat])
            lst_prob_tuple.append(prob_tuple)

    return util.sort_prob_tuples(lst_prob_tuple)


def get_cat_to_class(lst_prob_tuple, mu, lambda_, cat_lst):
    '''
    classify category tuples to three classes. first assign all cat to "possible match",
      then assign unmatch, finally match, to deal with cross-over.
    Inputs:
      lst_prob_tuple (list): a list of tuples of three elements - category tuple,
        match probability, and unmatch probability,
      mu (float) : the maximum false positive rate,
      lambda_ (float): the maximum false negative rate,
      cat_lst (list): list of all category tuples (in this pa, 27).
    Outputs:
      dct_cat_class (dict): a dictionary classifying category tuples to three classes
    '''
    dct_cat_class = dict.fromkeys(cat_lst, "possible match")
    sum_u = 0
    for i in range(len(lst_prob_tuple)):
        sum_u_update = sum_u + lst_prob_tuple[-i-1][1]
        if sum_u_update <= lambda_:
            sum_u = sum_u_update
            dct_cat_class[lst_prob_tuple[-i-1][0]] = "unmatch"
        else:
            break
    sum_u = 0       
    for i in range(len(lst_prob_tuple)):
        sum_u_update = sum_u + lst_prob_tuple[i][2]
        if sum_u_update <= mu:
            sum_u = sum_u_update
            dct_cat_class[lst_prob_tuple[i][0]] = "match"
        else:
            break
    return dct_cat_class
