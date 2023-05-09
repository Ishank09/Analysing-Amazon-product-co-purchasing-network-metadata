import re
import json
from time import sleep
from tqdm import tqdm
def parse_text_to_json(text):
    import re
    # global block regex
    pattern = r'(Id): ([^\n]+)\n(ASIN): ([^\n]+)(?:\n  (title): ([^\n]+))?(?:\n  (group): ([^\n]+))?(?:\n  (salesrank): ([^\n]+))?(?:\n  (similar): ([^\n]+))?(?:\n  (categories):([\s\S]*?)(?=\n\n|\n  reviews))?(?:\n  (reviews):([\s\S]*?)(?=\n\n|\n  Id))?'

    matches = re.findall(pattern, text)
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
                    value = [[x.strip() for x in t.split('|')] for t in value.strip().split('\n')[1:]]
                elif key == 'reviews':
                    reviews = {}
                    # review regex
                    review_pattern = r'\s*(total):\s+(\d+)\s+(downloaded):\s+(\d+)\s+(avg rating):\s+([\d\.]+)\n?\n?((?:\s{4}[^\n]*\n?)*)?'
                    review_matches = re.findall(review_pattern, value)
                    if review_matches:
                        for ri in range(len(review_matches[0])):
                            if ri==6:
                                rval = review_matches[0][ri]
                                revs = []
                                # customer review regex
                                cust_review_pattern = r'\s*(\d{4}-\d{1,2}-\d{1,2})\s+(cutomer):\s+(\w+)\s+(rating):\s+(\d+)\s+(votes):\s+(\d+)\s+(helpful):\s+(\d+)\s*'
                                cust_review_matches = re.findall(cust_review_pattern, rval)
                                if cust_review_matches:
                                    for cust_review_match in cust_review_matches:
                                        cus = {}
                                        for cri in range(len(cust_review_match)):
                                            if cri == 0:
                                                cus['date'] = cust_review_match[cri]
                                                continue
                                            if cri % 2 == 1:
                                                crkey = cust_review_match[cri]
                                            else:
                                                crvalue = cust_review_match[cri]
                                                if crkey == 'cutomer':
                                                    crvalue = crvalue
                                                elif crkey == 'rating':
                                                    crvalue = int(crvalue)
                                                elif crkey == 'votes':
                                                    crvalue = int(crvalue)
                                                elif crkey == 'helpful':
                                                    crvalue = int(crvalue)
                                                cus[crkey] = crvalue
                                        revs.append(cus)
                                
                                reviews['customer_reviews'] = revs
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
                   
                    value = reviews
                groups[key] = value
        resp.append(groups)

    with open("data/sample.json", "w") as file:
        json.dump(resp, file)
    groups = {}

data = ""
with open('data/amazon-meta.txt', 'r') as file:
    data = file.read()
parse_text_to_json(data)