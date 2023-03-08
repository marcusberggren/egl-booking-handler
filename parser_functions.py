import re

import fitz

"""
Functions for pdf_parser file.
"""

def get_value_in_rect(doc, total_words, search_str, rect_add=(0, 0, 0, 0)):
    try:
        rect = doc[0].search_for(search_str)[0] + rect_add
    except IndexError:
        print(f"Rect {search_str} not found.")
        return ""

    if rect:
        try:
            return re.match(r'^:*(.*)',' '.join([word[4] for word in total_words if fitz.Rect(word[:4]).intersects(rect)])).group(1)
        except IndexError:
            print(f"List comprehension for {search_str} not working.")
            return ""


def check_container_amount(string, list_of_containers):
    amount = len(list_of_containers)
    match_num = int(re.match(r'^\d+', string).group())
    if match_num == 1 and amount > 1:
        return amount
    else:
        return match_num


def get_container_type(string):
    c_type = re.match(r'^.*/(.+)', string).group(1)
    match c_type:
        case "40' HI-CUBE":
            return "45G1"
        case "40' STANDARD DRY":
            return "42G1"
        case "20' STANDARD DRY":
            return "22G1"
        case _:
            return "N/A"
            
def get_container_list(doc: fitz.Document, total_words: list, height: float, containers: list, container_list: list) -> list:
    for rect in containers:
        if rect:
            rect_upd = rect + (0, 3 + height, 0, -7 + height)
            list_comp = re.match(r'^:*(.*)',' '.join([word[4] for word in total_words if fitz.Rect(word[:4]).intersects(rect_upd)])).group(1)
            container_list.append(list_comp)
    return container_list

def extract_container_weight(string: str) -> float:
    # matches format like 150,000.00
    pattern = r'^\d{1,3}(,\d{3})*\.\d{2}'
    matching = re.search(pattern, string)
    if matching:
        return float(matching.group().replace(',', ''))
    else:
        return 0.0

def extract_tare_weight(string):
    # matches format at end of string like 25,200
    pattern = r'\d{1,3}(,\d{3})*$'
    match = re.search(pattern, string)
    if match:
        return float(match.group().replace(',', ''))
    else:
        return 0.0

def extract_final_pod(string):
    # matches all characters before the first comma after a colon
    pattern = r'^:*(.+?),'
    match = re.search(pattern, string)
    if match:
        return match.group(1)
    else:
        return None

def trim_date_string(string):
    # trim date string from 'DATE:' if there is any in the beginning
    pattern= r'^(DATE:)*(.*)$'
    match = re.search(pattern, string)
    if match:
        return match.group(2)
    else:
        return ""
    
def check_weights(gross_weight, tare_weight, container_amount):
    container_count = re.match(r'^\d+', container_amount).group()
    return (gross_weight + tare_weight)/ int(container_count)

def ocean_vessel_and_voy(string):
    matching = re.match(r'^VSL/VOY:*(\D+)\s([\d\w-]*)$', string)
    return {'vessel': matching.group(1), 'voy': matching.group(2)}

def departure_voyage():
    """TBC"""
    pass

def departure_week():
    """TBC"""
    pass
