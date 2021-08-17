"""
CAPP 30122: Course Search Engine Part 1

Yile CHEN
"""
# DO NOT REMOVE THESE LINES OF CODE
# pylint: disable-msg=invalid-name, redefined-outer-name, unused-argument, unused-variable

import queue
import json
import sys
import csv
import re
import bs4
import util

INDEX_IGNORE = set(['a', 'also', 'an', 'and', 'are', 'as', 'at', 'be',
                    'but', 'by', 'course', 'for', 'from', 'how', 'i',
                    'ii', 'iii', 'in', 'include', 'is', 'not', 'of',
                    'on', 'or', 's', 'sequence', 'so', 'social', 'students',
                    'such', 'that', 'the', 'their', 'this', 'through', 'to',
                    'topics', 'units', 'we', 'were', 'which', 'will', 'with',
                    'yet'])


def get_soup(url):
    """
    Get the soup of an url.

    Inputs:
        Url: the url of interest

    Outputs:
        Soup: soup of the url or None if nothing is attained.    
    """
    r = util.get_request(url)
    if r != None:
        p = util.read_request(r)
        if len(p) != 0:
            soup = bs4.BeautifulSoup(p, "html5lib")
            return soup
        else:
            return None
    else:
        return None

def put_urls(soup, url_visited, q, url, limiting_domain):
    """
    Get the urls in the visited page, and put them in the queue.

    Inputs:
        soup: the soup of the visited page
        url_visited: list of urls that have been visited
        q：the queue of urls waiting to be visited
        url: the visited url, i.e., starting url, relative to the urls in it
        limiting_domain: the specific domain that urls should fall within

    Outputs:
        no output
    """
    a = soup.find_all('a')
    if len(a) != 0:
        for t in a:
            if t.has_attr('href'):
                url_in = util.remove_fragment(t['href'])
                url_in = util.convert_if_relative_url(url, url_in)
                if util.is_url_ok_to_follow(url_in, limiting_domain) and url_in not in url_visited:
                    url_visited.append(url_in)
                    q.put(url_in)

def put_codetoword(soup, dict_codetoword):
    """
    Put the course code and the word indexer pairs in a dictionary

    Inputs:
        soup: the soup of the visited page
        dict_coodetoword: the dictionary mapping course code to lst of word indexers

    Outputs:
        no output
    """
    divs = soup.find_all('div', class_="courseblock main")
    for div in divs:
        subsequence = util.find_sequence(div)
        title = div.find_all('p', class_ = "courseblocktitle")[0].text
        des = div.find_all('p', class_= "courseblockdesc")[0].text
        if len(util.find_sequence(div)) == 0: 
                code = re.findall(r'\w{4}.\d{5}', title)[0] 
                code = code[0:4] + " " + code[5:11]
                lst_word = re.findall(r'[a-zA-Z]+[a-zA-Z\d/_]*', des+title)
                if code not in dict_codetoword:
                    dict_codetoword[code] = lst_word
        else:
                lst_wordtitle = re.findall(r'[a-zA-Z]+[a-zA-Z\d/_]*', des+title)
                for s in subsequence:
                    title_s = s.find_all('p', class_ = "courseblocktitle")[0].text
                    des_s = s.find_all('p', class_= "courseblockdesc")[0].text
                    code_s = re.findall(r'\w{4}.\d{5}', title_s)[0]
                    code_s = code_s[0:4] + " " + code_s[5:11]
                    lst_word = re.findall(r'[a-zA-Z]+[a-zA-Z\d/_]*', des_s+title_s) + lst_wordtitle
                    if code_s not in dict_codetoword:
                        dict_codetoword[code_s] = lst_word

def get_indexer(dict_codetoindex, dict_codetoword):
    """
    Get a lst of indexers - course identifier and a word

    Inputs:
        dict_codetoindex: the dictionary mapping course code to course identifier
        dict_coodetoword: the dictionary mapping course code to lst of word indexers

    Outputs:
        lst_indextoword: a lst of indexers - course identifier and a word
    """
    lst_indextoword = []
    for code, wordlist in dict_codetoword.items():
        dedup = []
        for word in wordlist:
            word = word.lower()
            if word not in dedup and word not in INDEX_IGNORE:
                indexer = [str(dict_codetoindex[code]) + '|' + word]
                lst_indextoword.append(indexer)
                dedup.append(word)
    return lst_indextoword


def go(num_pages_to_crawl, course_map_filename, index_filename):
    '''
    Crawl the college catalog and generates a CSV file with an index.

    Inputs:
        num_pages_to_crawl: the number of pages to process during the crawl
        course_map_filename: the name of a JSON file that contains the mapping
          course codes to course identifiers
        index_filename: the name for the CSV of the index.

    Outputs:
        CSV file of the index index.
    '''

    starting_url = ("http://www.classes.cs.uchicago.edu/archive/2015/winter"
                    "/12200-1/new.collegecatalog.uchicago.edu/index.html")
    limiting_domain = "classes.cs.uchicago.edu"

    file = open(course_map_filename,) 
    dict_codetoindex = json.load(file)

    num_page_visited = 0
    q = queue.Queue()
    q.put(starting_url)
    url_visited = []
    dict_codetoword = {}

    while num_page_visited < num_pages_to_crawl:
        url = q.get()
        soup = get_soup(url)
        if soup != None:
            put_urls(soup, url_visited, q, url, limiting_domain)
            put_codetoword(soup, dict_codetoword)
        num_page_visited += 1
        if q.empty():
            break

    lst_indexer = get_indexer(dict_codetoindex, dict_codetoword)

    with open(index_filename, 'w') as csvfile:  
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(lst_indexer)

if __name__ == "__main__":
    usage = "python3 crawl.py <number of pages to crawl>"
    args_len = len(sys.argv)
    course_map_filename = "course_map.json"
    index_filename = "catalog_index.csv"
    if args_len == 1:
        num_pages_to_crawl = 1000
    elif args_len == 2:
        try:
            num_pages_to_crawl = int(sys.argv[1])
        except ValueError:
            print(usage)
            sys.exit(0)
    else:
        print(usage)
        sys.exit(0)

    go(num_pages_to_crawl, course_map_filename, index_filename)
