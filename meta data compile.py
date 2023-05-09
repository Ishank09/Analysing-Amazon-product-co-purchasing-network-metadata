import re
import json
from time import sleep
from tqdm import tqdm

def match_customer_review_pattern(value):
    # customer review regex
    CUST_REVIEW_PATTERN = r'\s*(\d{4}-\d{1,2}-\d{1,2})\s+(cutomer):\s+(\w+)\s+(rating):\s+(\d+)\s+(votes):\s+(\d+)\s+(helpful):\s+(\d+)\s*'
    cust_review_matches = re.findall(CUST_REVIEW_PATTERN, value)
    return cust_review_matches


def check_customer_review_pattern(value, revs):
    cust_review_matches = match_customer_review_pattern(value)
    if cust_review_matches:
        for cust_review_match in cust_review_matches:
            cus = parse_customer_review_match(cust_review_match)
            revs.append(cus)
    return revs

def handle_customer_review_key(crkey, crvalue):
    if crkey == 'rating' or crkey == 'votes' or crkey == 'helpful':
        return int(crvalue)
    else:
        try:
            return float(crvalue)
        except ValueError:
            return crvalue


def parse_customer_review_match(cust_review_match):
    cus = {}
    crkey = ""
    crvalue = None
    for cri in range(len(cust_review_match)):
        if cri == 0:
            cus['date'] = cust_review_match[cri]
            continue
        if cri % 2 == 1:
            crkey = cust_review_match[cri]
        else:
            crvalue = cust_review_match[cri]
            crvalue = handle_customer_review_key(crkey, crvalue)
            cus[crkey] = crvalue
    return cus


    
def match_check_review_pattern(value):
    REVIEW_PATTERN = r'\s*(total):\s+(\d+)\s+(downloaded):\s+(\d+)\s+(avg rating):\s+([\d\.]+)\n?\n?((?:\s{4}[^\n]*\n?)*)?'
    review_matches = re.findall(REVIEW_PATTERN, value)
    return review_matches

def check_review_pattern(value, reviews):
    review_matches = match_check_review_pattern(value)
    if review_matches:
        for ri in range(len(review_matches[0])):
            if ri==6:
                rval = review_matches[0][ri]
                revs = []
                
                reviews['customer_reviews'] = check_customer_review_pattern(rval, revs)
                break
            if ri % 2 == 0:
                rkey = review_matches[0][ri]
            else:
                rvalue = review_matches[0][ri]
                if rkey == 'total':
                    rvalue = int(rvalue)
                elif rkey == 'downloaded':
                    rvalue = int(rvalue)
                elif rkey == 'avg rating':
                    rvalue = rvalue
                reviews[rkey] = rvalue
    return reviews
    
def match_global_block_pattern(value):
    GLOBAL_BLOCK_PATTERN = r'(Id): ([^\n]+)\n(ASIN): ([^\n]+)(?:\n  (title): ([^\n]+))?(?:\n  (group): ([^\n]+))?(?:\n  (salesrank): ([^\n]+))?(?:\n  (similar): ([^\n]+))?(?:\n  (categories):([\s\S]*?)(?=\n\n|\n  reviews))?(?:\n  (reviews):([\s\S]*?)(?=\n\n|\n  Id))?'
    matches = re.findall(GLOBAL_BLOCK_PATTERN, value)
    return matches

def parse_text_to_json(text):

    matches = match_global_block_pattern(text)
    resp = []
    groups = {}

    for match in tqdm(matches):
        groups = {}
        for i in range(len(match)):
            if i % 2 == 0:
                key = match[i]
            else:
                value = match[i]
                if key == 'Id':
                    value = int(value)
                    if value == 7:
                        print('hi')
                elif key == 'salesrank':
                    value = int(value)
                elif key == 'similar':
                    value = value.split()[1:]
                elif key == 'categories':
                    value = [[x.strip() for x in t.split('|') if x.strip()] for t in value.strip().split('\n')[1:]]
                elif key == 'reviews':
                    reviews = {}
                    # review regex
                    value = check_review_pattern(value, reviews)
                if key is not None and value is not None and str(key).strip() and str(value).strip():
                    groups[key] = value

        resp.append(groups)

    with open("data/sample.json", "w") as file:
        json.dump(resp, file)
    groups = {}

data = ""
with open('data/sample.txt', 'r') as file:
    data = file.read()
parse_text_to_json(data)