import re
import json
from time import sleep
from tqdm import tqdm

def match_customer_review_pattern(value):
    """
    Matches customer review pattern in the given value using regex.
    
    Args:
        value (str): The string to search for customer review pattern.
        
    Returns:
        list: List of matches found in the value.
    """
    CUST_REVIEW_PATTERN = r'\s*(\d{4}-\d{1,2}-\d{1,2})\s+(cutomer):\s+(\w+)\s+(rating):\s+(\d+)\s+(votes):\s+(\d+)\s+(helpful):\s+(\d+)\s*'
    cust_review_matches = re.findall(CUST_REVIEW_PATTERN, value)
    return cust_review_matches

def check_customer_review_pattern(value, revs):
    """
    Checks customer review pattern in the given value and appends the parsed customer reviews to the revs list.
    
    Args:
        value (str): The string to check for customer review pattern.
        revs (list): The list to append the parsed customer reviews.
        
    Returns:
        list: List of customer reviews appended to the revs list.
    """
    cust_review_matches = match_customer_review_pattern(value)
    if cust_review_matches:
        for cust_review_match in cust_review_matches:
            cus = parse_customer_review_match(cust_review_match)
            revs.append(cus)
    return revs

def handle_customer_review_key(crkey, crvalue):
    """
    Handles the conversion of customer review key values to appropriate data types.
    
    Args:
        crkey (str): The customer review key.
        crvalue (str): The customer review value.
        
    Returns:
        int or float or str: The converted value based on the key.
    """
    if crkey == 'rating' or crkey == 'votes' or crkey == 'helpful':
        return int(crvalue)
    else:
        try:
            return float(crvalue)
        except ValueError:
            return crvalue

def parse_customer_review_match(cust_review_match):
    """
    Parses the matched customer review and returns a dictionary with key-value pairs.
    
    Args:
        cust_review_match (tuple): The matched customer review values.
        
    Returns:
        dict: Parsed customer review with key-value pairs.
    """
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
    """
    Matches the review pattern in the given value using regex.
    
    Args:
        value (str): The string to search for review pattern.
        
    Returns:
        list: List of matches found in the value.
    """
    REVIEW_PATTERN = r'\s*(total):\s+(\d+)\s+(downloaded):\s+(\d+)\s+(avg rating):\s+([\d\.]+)\n?\n?((?:\s{4}[^\n]*\n?)*)?'
    review_matches = re.findall(REVIEW_PATTERN, value)
    return review_matches

def check_review_pattern(value, reviews):
    """
    This function checks if the given value matches the review pattern. If it does, it returns a dictionary of the review data.

    Args:
        value (str): The value to check.
        reviews (dict): The dictionary to store the review data in.

    Returns:
        dict: The dictionary of the review data, or None if the value does not match the review pattern.
    """

    review_matches = match_check_review_pattern(value)
    if review_matches:
        for ri in range(len(review_matches[0])):
            if ri == 6:
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
    """
    This function matches the global block pattern in the given value.

    Args:
        value (str): The value to match.

    Returns:
        list: A list of matches, or None if the value does not match the pattern.
    """

    GLOBAL_BLOCK_PATTERN = r'(Id): ([^\n]+)\n(ASIN): ([^\n]+)(?:\n  (title): ([^\n]+))?(?:\n  (group): ([^\n]+))?(?:\n  (salesrank): ([^\n]+))?(?:\n  (similar): ([^\n]+))?(?:\n  (categories):([\s\S]*?)(?=\n\n|\n  reviews))?(?:\n  (reviews):([\s\S]*?)(?=\n\n|\n  Id))?'
    matches = re.findall(GLOBAL_BLOCK_PATTERN, value)
    return matches

def parse_text_to_json(text):
    """
    This function parses the given text into a JSON object.

    Args:
        text (str): The text to parse.

    Returns:
        dict: The JSON object, or None if the text could not be parsed.
    """

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
        return resp

    with open("data/sample.json", "w") as file:
        json.dump(resp, file)
    groups = {}




if __name__ == "__main__":
    data = ""
    with open('data/amazon-meta.txt', 'r') as file:
        data = file.read()
    parse_text_to_json(data)
