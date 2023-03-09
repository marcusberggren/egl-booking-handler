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
rect_container_nwt = "" #(-24, 10, -102, 0)
rect_container_tare = "" #(-24, 10, -102, 0)


#file_path= r'bokningar_pdf\special\SB2LBDHY.PDF'           
file_path= r'bokningar_pdf\special\SB2LCV65.PDF'               # (1x40HC) * 6
#file_path= r'bokningar_pdf\special\SBBXNCPY.pdf'               # 22x40HC  
#file_path= r'bokningar_pdf\special\SB2SS6YS - 20 + 40.PDF'      # 1x40DV, 1x20DV   



with open(file_path) as f:
    doc = fitz.open(f)

total_height = 0.0
total_words = []
list_count_40hc, list_count_40dv, list_count_20dv = [], [], []
list_tare_40hc, list_tare_40dv, list_tare_20dv = [], [], []
list_nwt_40hc, list_nwt_40dv, list_nwt_20dv = [], [], []

for page in doc:
    word_list = page.get_text('words')
    for word in word_list:
        total_words.append([word[0], word[1] + total_height, word[2], word[3] + total_height, word[4]])

    d20 = page.search_for(CONTAINER_20DV)
    d40 = page.search_for(CONTAINER_40DV)
    h40 = page.search_for(CONTAINER_40HC)

    list_count_40hc.append(pf.get_container_info(total_words, h40, rect_container_hc, total_height))
    list_count_40dv.append(pf.get_container_info(total_words, d40, rect_container_dv, total_height))
    list_count_20dv.append(pf.get_container_info(total_words, d20, rect_container_dv, total_height))

    list_tare_40hc.append(pf.get_container_info(total_words, h40, rect_container_tare, total_height))
    list_tare_40dv.append(pf.get_container_info(total_words, d40, rect_container_tare, total_height))
    list_tare_20dv.append(pf.get_container_info(total_words, d20, rect_container_tare, total_height))

    list_nwt_40hc.append(pf.get_container_info(total_words, h40, rect_container_nwt, total_height))
    list_nwt_40dv.append(pf.get_container_info(total_words, d40, rect_container_nwt, total_height))
    list_nwt_20dv.append(pf.get_container_info(total_words, d20, rect_container_nwt, total_height))

    total_height += page.rect.height


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
#container_info = pf.get_value_in_rect(doc, total_words, CONTAINER_INFO, rect_container_info)
#container_weight = pf.get_value_in_rect(doc, total_words, CONTAINER_WEIGHT, rect_container_weight)
#container_tare = pf.get_value_in_rect(doc, total_words, CONTAINER_TARE, rect_container_tare)
#dangerous_cargo = pf.get_value_in_rect(doc, total_words, DANGEROUS_CARGO, rect_dangerous_cargo)
container_40hc = pf.get_value_in_rect(doc, total_words, CONTAINER_40HC, rect_container_hc)
container_40dv = pf.get_value_in_rect(doc, total_words, CONTAINER_40DV, rect_container_dv)
container_20dv = pf.get_value_in_rect(doc, total_words, CONTAINER_20DV, rect_container_dv)


return_dict = {
    'booking_revised': booking_revised,
    'date_booked': pf.trim_date_string(date_booked),
    'booking_number': booking_number,
    'departure_week': departure_voy,
    'departure_date': departure_date,
    'discharge_port': discharge_port,
    #'mother_vessel': mother_vessel,
    'ocean_vessel': pf.ocean_vessel_and_voy(mother_vessel)['vessel'],
    'voyage': pf.ocean_vessel_and_voy(mother_vessel)['voy'],
    'stowage_code': stowage_code,
    'final_pod': pf.extract_final_pod(final_pod),
    'commodity': commodity,
    'discharge_terminal': discharge_terminal,   #endast "godkända" terminaler ska tas med
    #'container_info': container_info,
    'container_amount': {'40hc': pf.container_counter(list_count_40hc),
                         '40dv': pf.container_counter(list_count_40dv),
                         '20dv': pf.container_counter(list_count_20dv)},
    #'container_type': pf.get_container_type(container_info),
    'weights': {'nwt': {'40hc': "",
                        '40dv': "",
                        '20dv': ""
                        },
                'tare': {'40hc': "",
                        '40dv': "",
                        '20dv': ""
                        },
                'gwt': {'40hc': "",
                        '40dv': "",
                        '20dv': ""
                        }
                },
    #'final_weight': pf.check_weights(pf.extract_container_weight(container_weight), pf.extract_tare_weight(container_tare), container_info),
    #'container_weight': pf.extract_container_weight(container_weight),
    #'container_tare': pf.extract_tare_weight(container_tare),
    #'dangerous_cargo': dangerous_cargo.strip('()')
}

for key, value in return_dict.items():
    print(f'{key}: {value}')
