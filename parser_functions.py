import itertools
import re

import fitz

"""
Functions for pdf_parser file.
"""

def get_value_in_rect(doc, total_words, search_str, rect_add=(0, 0, 0, 0)):
    try:
        rect = doc[0].search_for(search_str)[0] + rect_add
    except IndexError:
        #print(f"Rect {search_str} not found.")
        return ""

    if rect:
        try:
            return re.match(r'^:*(.*)',' '.join([word[4] for word in total_words if fitz.Rect(word[:4]).intersects(rect)])).group(1)
        except IndexError:
            #print(f"List comprehension for {search_str} not working.")
            return ""

    
def get_container_amount(total_words, rect_list, rect_add, height):
    list_count = []
    for rect in rect_list:
        rect = rect + rect_add + (0, height, 0, height)
        result = re.sub(r'^\+*', '',''.join([word[4] for word in total_words if fitz.Rect(word[:4]).intersects(rect)])).replace(',', '')
        list_count.append(float(result))
    return list_count

def get_container_info(total_words, rect_list, rect_add, height):
    list_count_nwt = []
    list_count_tare = []
    for rect in rect_list:
        rect = rect + rect_add + (0, height, 0, height)
        result = re.match(r'(\d{1,4},\d{3}.\d{2})*(\+*\d{1,3},\d{3})*',
                          ''.join([word[4] for word in total_words if fitz.Rect(word[:4]).intersects(rect)]))
        result_nwt = result.group(1)
        result_tare = result.group(2)

        if result_nwt is not None:
            result_nwt = re.sub(r',*\+*', '', result_nwt)
        else:
            result_nwt = 0
        if result_tare is not None:
            result_tare = re.sub(r',*\+*', '', result_tare)
        else:
            result_tare = 0
        
        list_count_nwt.append(float(result_nwt))
        list_count_tare.append(float(result_tare))

    return list_count_nwt, list_count_tare

def get_container_hazards(total_words, rect_list, rect_add, height):
    list_count = ""
    for rect in rect_list:
        rect = rect + rect_add + (0, height, 0, height)
        list_count += re.sub(r'[()]', ' ', ''.join([word[4] for word in total_words if fitz.Rect(word[:4]).intersects(rect)]))
    return list_count.split()

def create_hazards_list(hazards_list:list) -> list:
    unique_list = concatenate_list(hazards_list)
    return list(set(unique_list))
    

def concatenate_floats(*lists:list) -> float:
    concatenated_list = itertools.chain.from_iterable(*lists)
    summa = float(sum(concatenated_list))
    return round(summa, 2)
    
def concatenate_list(*lists):
    return itertools.chain.from_iterable(*lists)


def calculate_weights(weight_list:list, container_list:list) -> float:
    container_amount = concatenate_floats(container_list)
    if container_amount == 0:
        return 0.00
    else:
        return float(concatenate_floats(weight_list))/container_amount


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
    

def ocean_vessel_and_voy(string):
    matching = re.match(r'^VSL/VOY:*(\D+)\s([\d\w-]*)$', string)
    return {'vessel': matching.group(1), 'voy': matching.group(2)}


def departure_voyage():
    """TBC"""
    pass

def departure_week():
    """TBC"""
    pass
