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
rect_booking_number = (130, 2, 200, -7)
rect_departure_week = (130, 3, 250, -7)
rect_departure_date = (108, 3, 160, -7)
rect_discharge_port = (132, 3, 160, -7)
rect_mother_vessel = (48, 3, 250, -7)
rect_stowage_code = (84, 3, 100, -7)
rect_final_pod = (132, 3, 300, -7)
rect_commodity = (132, 3, 350, -7)
rect_discharge_terminal = (132, 3, 200, -7)
rect_container_info = (0, 26, 42, 26)
rect_container_weight = (0, 26, 6, 26)
rect_container_tare = (12, 26, 0, 26)
rect_dangerous_cargo = (18, 26, 36, 26)

file_path= r'bokningar_pdf\special\SB2LBDHY.PDF'
total_height = 0.0
total_words = []

with open(file_path) as f:
    doc = fitz.open(f)

for page in doc:
    word_list = page.get_text('words')
    for word in word_list:
        total_words.append([word[0], word[1] + total_height, word[2], word[3] + total_height, word[4]])
    total_height += page.rect.height


def get_value_in_rect(search_str, rect_add):

    try:
        rect = doc[0].search_for(search_str)[0] + rect_add
    except:
        print(f"Rect {search_str} not found.")
        return ""

    if rect:
        try:
            return [word[4] for word in total_words if fitz.Rect(word[:4]).intersects(rect)]
        except:
            print(f"List comprehension for {search_str} not working.")
            return ""

booking_revised = get_value_in_rect(BOOKING_REVISED, rect_booking_revised)
date_booked = get_value_in_rect(DATE_BOOKED, rect_date_booked)
booking_number = get_value_in_rect(BOOKING_NUMBER, rect_booking_number)
departure_week = get_value_in_rect(DEPARTURE_WEEK, rect_departure_week)
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

return_dict = {
    'booking_revised': booking_revised,
    'date_booked': date_booked[0],
    'time_booked': date_booked[1],
    'booking_number': booking_number,
    'departure_week': departure_week,
    'departure_date': departure_date,
    'discharge_port': discharge_port,
    'mother_vessel': mother_vessel,
    'stowage_code': stowage_code,
    'final_pod': final_pod,
    'commodity': commodity,
    'discharge_terminal': discharge_terminal,
    'container_info': container_info,
    'container_weight': container_weight,
    'container_tare': container_tare,
    'dangerous_cargo': dangerous_cargo
}

print(return_dict['container_info'])
