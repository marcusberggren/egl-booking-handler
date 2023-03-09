import re

import fitz

import parser_functions as pf

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
CONTAINER_40HC = "40' HI-CUBE"
CONTAINER_40DV = "40' STANDARD DRY"
CONTAINER_20DV = "20' STANDARD DRY"
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
rect_container_hc = (-24, 10, -72, 0)
rect_container_dv = (-24, 10, -102, 0)

#file_path= r'bokningar_pdf\special\SB2LBDHY.PDF'           
file_path= r'bokningar_pdf\special\SB2LCV65.PDF'               # (1x40HC) * 6
#file_path= r'bokningar_pdf\special\SBBXNCPY.pdf'               # 22x40HC  
#file_path= r'bokningar_pdf\special\SB2SS6YS - 20 + 40.PDF'      # 1x40DV, 1x20DV   
total_height = 0.0
total_words = []
search_20dv = ""
search_40dv = ""
search_40hc = ""
container_types = {'20dv': 0, '40dv': 0, '40hc': 0}

with open(file_path) as f:
    doc = fitz.open(f)

def get_container_amount(rect_list, rect_add, height):
    for rect in rect_list:
        rect += rect_add #+ (0, height, 0, height)
        #return [word[4] for word in total_words if fitz.Rect(word[:4]).intersects(rect)]

test = []

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

    test = get_container_amount(h40, rect_container_hc, total_height)

    print(test)



#print("1)", page.search_for("4,166.67"))
#print("1)", page.search_for("10,000.00"))
#print("1)", page.search_for("550,000.00"))
#print("2)", page.search_for("+4,200"))
#print("2)", page.search_for("+2,400"))
#print("2)", page.search_for("+92,400"))
#print("3)", page.search_for("(NON-HAZARDOUS)"))
#print("4)", d20, d40, h40)

print(container_types)


booking_revised = pf.get_value_in_rect(doc, total_words, BOOKING_REVISED, rect_booking_revised)
date_booked = pf.get_value_in_rect(doc, total_words, DATE_BOOKED, rect_date_booked)
booking_number = pf.get_value_in_rect(doc, total_words, BOOKING_NUMBER, rect_booking_number)
departure_voy = pf.get_value_in_rect(doc, total_words, DEPARTURE_WEEK, rect_departure_week)
departure_date = pf.get_value_in_rect(doc, total_words, DEPARTURE_DATE, rect_departure_date)
discharge_port = pf.get_value_in_rect(doc, total_words, DISCHARGE_PORT, rect_discharge_port)
mother_vessel = pf.get_value_in_rect(doc, total_words, MOTHER_VESSEL, rect_mother_vessel)
stowage_code = pf.get_value_in_rect(doc, total_words, STOWAGE_CODE, rect_stowage_code)
final_pod = pf.get_value_in_rect(doc, total_words, FINAL_POD, rect_final_pod)
commodity = pf.get_value_in_rect(doc, total_words, COMMODITY, rect_commodity)
discharge_terminal = pf.get_value_in_rect(doc, total_words, DISCHARGE_TERMINAL, rect_discharge_terminal)
container_info = pf.get_value_in_rect(doc, total_words, CONTAINER_INFO, rect_container_info)
container_weight = pf.get_value_in_rect(doc, total_words, CONTAINER_WEIGHT, rect_container_weight)
container_tare = pf.get_value_in_rect(doc, total_words, CONTAINER_TARE, rect_container_tare)
dangerous_cargo = pf.get_value_in_rect(doc, total_words, DANGEROUS_CARGO, rect_dangerous_cargo)
container_40hc = pf.get_value_in_rect(doc, total_words, CONTAINER_40HC, rect_container_hc)
container_40dv = pf.get_value_in_rect(doc, total_words, CONTAINER_40DV, rect_container_dv)
container_20dv = pf.get_value_in_rect(doc, total_words, CONTAINER_20DV, rect_container_dv)

print(container_20dv, container_40dv, container_40hc)

containers = ""
container_list = []
height = 0.0
search_20dv = ""
search_40dv = ""
search_40hc = ""

"""
Another loop to find if for example "1 /40' HI-CUBE" exists in more places than one. If it does then it collects them in a list and  
"""

list_of_40hc = []
list_of_40dv = []
list_of_20dv = []

for page in doc:
    _40hc = page.search_for("40' HI-CUBE")
    _40dv = page.search_for("40' STANDARD DRY")
    _20dv = page.search_for("20' STANDARD DRY")

    pf.get_container_list(doc, total_words, height, _40hc, list_of_40hc)
    pf.get_container_list(doc, total_words, height, _40dv, list_of_40dv)
    pf.get_container_list(doc, total_words, height, _20dv, list_of_20dv)

    height += page.rect.height


"""print(list_of_40hc)
print(list_of_40dv)
print(list_of_20dv)"""


#container_amount = len(container_list)


return_dict = {
    'booking_revised': booking_revised,
    'date_booked': pf.trim_date_string(date_booked),
    'booking_number': booking_number,
    'departure_week': departure_voy,
    'departure_date': departure_date,
    'discharge_port': discharge_port,
    'mother_vessel': mother_vessel,
    'ocean_vessel': pf.ocean_vessel_and_voy(mother_vessel)['vessel'],
    'voyage': pf.ocean_vessel_and_voy(mother_vessel)['voy'],
    'stowage_code': stowage_code,
    'final_pod': pf.extract_final_pod(final_pod),
    'commodity': commodity,
    'discharge_terminal': discharge_terminal,   #endast "godkända" terminaler ska tas med
    'container_info': container_info,
    'container_amount': {'40hc': pf.check_container_amount(container_info, list_of_40hc),
                         '40dv': pf.check_container_amount(container_info, list_of_40dv),
                         '20dv': pf.check_container_amount(container_info, list_of_20dv)},
    'container_type': pf.get_container_type(container_info),
    'weights': {'total_nwt': '',
                'total_tare': '',
                'total_gwt': '',
                'total_weight_per_unit': '',
                },
    'final_weight': pf.check_weights(pf.extract_container_weight(container_weight), pf.extract_tare_weight(container_tare), container_info),
    'container_weight': pf.extract_container_weight(container_weight),
    'container_tare': pf.extract_tare_weight(container_tare),
    'dangerous_cargo': dangerous_cargo.strip('()')
}

for key, value in return_dict.items():
    print(f'{key}: {value}')
