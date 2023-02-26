import re

import fitz

BOOKING_REVISED = "/ REVISE :"
DATE_BOOKED = "DATE:"
BOOKING_NUMBER = "BOOKING NO."
DEPARTURE_WEEK = "VESSEL/VOYAGE"
DEPARTURE_DATE = "ETD DATE"
DISCHARGE_PORT = "T/S PORT"
MOTHER_VESSEL = "VSL/VOY:"
STOWAGE_CODE = "STOWAGE CODE :"
FINAL_POD = "PORT OF DISCHARGING"
COMMODITY = "COMMODITY"
DISCHARGE_TERMINAL = "REMARKS"
CONTAINER_INFO = "QTY/TYPE"
CONTAINER_WEIGHT = "GWT+TARE"
CONTAINER_TARE = "WT(KGS)"
DANGEROUS_CARGO = "IMO CLASS/UN"

"""
booking_revised = " 000 "
date_booked = "2023/02/21 10:31:27"
booking_number = "503300003126"
departure_week = "To Be Advised 011S"
departure_date = "2023/03/16"
discharge_port = "ROTTERDAM"
mother_vessel = "THALASSA TYHI 0642-042E"
stowage_code = "EMX"
final_pod = "PORT KLANG WEST PORT,MALAYSIA"
commodity = "FOREST PRODUCTS"
discharge_terminal = "EMX"
container_info = "1 /40' HI-CUBE"
container_weight = "23,450.00"
container_tare = "4,200"
dangerous_cargo = "(NON-HAZARDOUS)"
"""

rect_booking_revised = (66, 0, 24, 0)
rect_date_booked = (36, 0, 120, 0)
rect_booking_number = (130, 2, 150, -7)
rect_departure_week = (130, 3, 250, -7)
rect_departure_date = (108, 3, 160, -7)
rect_discharge_port = (132, 3, 120, -7)
rect_mother_vessel = (48, 3, 250, -7)
rect_stowage_code = (84, 3, 100, -7)
rect_final_pod = (132, 3, 300, -7)
rect_commodity = (132, 3, 350, -7)
rect_discharge_terminal = (132, 3, 200, -7)
rect_container_info = (0, 29, 100, 19)
rect_container_weight = (-5, 29, 6, 19)
rect_container_tare = (12, 29, 10, 19)
rect_dangerous_cargo = (18, 29, 36, 19)

#file_path= r'bokningar_pdf\special\SB2LBDHY.PDF'
file_path= r'bokningar_pdf\special\SB2LCV65.PDF'
total_height = 0.0
total_words = []
search_20dv = ""
search_40dv = ""
search_40hc = ""
container_types = {'20dv': 0, '40dv': 0, '40hc': 0}

with open(file_path) as f:
    doc = fitz.open(f)

for page in doc:
    word_list = page.get_text('words')
    for word in word_list:
        total_words.append([word[0], word[1] + total_height, word[2], word[3] + total_height, word[4]])

    d20 = page.search_for("20' STANDARD DRY")
    d40 = page.search_for("40' STANDARD DRY")
    h40 = page.search_for("40' HI-CUBE")

    total_height += page.rect.height


    container_types['20dv'] += len(d20)
    container_types['40dv'] += len(d40)
    container_types['40hc'] += len(h40)



def get_value_in_rect(search_str, rect_add=(0, 0, 0, 0)):
    try:
        rect = doc[0].search_for(search_str)[0] + rect_add
    except:
        print(f"Rect {search_str} not found.")
        return ""

    if rect:
        try:
            return re.match(r'^:*(.*)',' '.join([word[4] for word in total_words if fitz.Rect(word[:4]).intersects(rect)])).group(1)
        except:
            print(f"List comprehension for {search_str} not working.")
            return ""

booking_revised = get_value_in_rect(BOOKING_REVISED, rect_booking_revised)
date_booked = get_value_in_rect(DATE_BOOKED, rect_date_booked)
booking_number = get_value_in_rect(BOOKING_NUMBER, rect_booking_number)
departure_voy = get_value_in_rect(DEPARTURE_WEEK, rect_departure_week)
departure_date = get_value_in_rect(DEPARTURE_DATE, rect_departure_date)
discharge_port = get_value_in_rect(DISCHARGE_PORT, rect_discharge_port)
mother_vessel = get_value_in_rect(MOTHER_VESSEL, rect_mother_vessel)
stowage_code = get_value_in_rect(STOWAGE_CODE, rect_stowage_code)
final_pod = get_value_in_rect(FINAL_POD, rect_final_pod)
commodity = get_value_in_rect(COMMODITY, rect_commodity)
discharge_terminal = get_value_in_rect(DISCHARGE_TERMINAL, rect_discharge_terminal)
container_info = get_value_in_rect(CONTAINER_INFO, rect_container_info)
container_weight = get_value_in_rect(CONTAINER_WEIGHT, rect_container_weight)
container_tare = get_value_in_rect(CONTAINER_TARE, rect_container_tare)
dangerous_cargo = get_value_in_rect(DANGEROUS_CARGO, rect_dangerous_cargo)

containers = ""
container_list = []
height = 0.0
search_20dv = ""
search_40dv = ""
search_40hc = ""

"""
Another loop to find if for example "1 /40' HI-CUBE" exists in more places than one. If it does then it collects them in a list and  
"""

for page in doc:
    containers = page.search_for(container_info)
    search_40hc = page.search_for("40' HI-CUBE")
    search_40dv = page.search_for("40' STANDARD DRY")
    search_20dv = page.search_for("20' STANDARD DRY")
    print(containers)

    for rect in containers:
        rect_upd = rect + (0, 3 + height, 0, -7 + height)
        list_comp = re.match(r'^:*(.*)',' '.join([word[4] for word in total_words if fitz.Rect(word[:4]).intersects(rect_upd)])).group(1)
        container_list.append(list_comp)
    height += page.rect.height

container_amount = len(container_list)



def check_container_amount(string, amount):
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
            return ""
            

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
    pass

def departure_week():
    pass


return_dict = {
    'booking_revised': booking_revised,
    'date_booked': trim_date_string(date_booked),
    'booking_number': booking_number,
    'departure_week': departure_voy,
    'departure_date': departure_date,
    'discharge_port': discharge_port,
    'mother_vessel': mother_vessel,
    'ocean_vessel': ocean_vessel_and_voy(mother_vessel)['vessel'],
    'voyage': ocean_vessel_and_voy(mother_vessel)['voy'],
    'stowage_code': stowage_code,
    'final_pod': extract_final_pod(final_pod),
    'commodity': commodity,
    'discharge_terminal': discharge_terminal,   #endast "godkända" terminaler ska tas med
    'container_info': container_info,
    'container_amount': check_container_amount(container_info, container_amount),
    'container_type': get_container_type(container_info),
    'weights': {'total_nwt': '',
                'total_tare': '',
                'total_gwt': '',
                'total_weight_per_unit': '',
                },
    'final_weight': check_weights(extract_container_weight(container_weight), extract_tare_weight(container_tare), container_info),
    'container_weight': extract_container_weight(container_weight),
    'container_tare': extract_tare_weight(container_tare),
    'dangerous_cargo': dangerous_cargo.strip('()')
}

print(return_dict)
