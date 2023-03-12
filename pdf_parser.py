import os
from datetime import datetime

import fitz
from tqdm import tqdm

import parser_functions as pf

BOOKING_REVISED = "/ REVISE :"
DATE_BOOKED = "DATE:"
BOOKING_NUMBER = "BOOKING NO."
DEPARTURE_WEEK = "VESSEL/VOYAGE"
DEPARTURE_DATE = "ETD DATE"
DISCHARGE_PORT = "T/S PORT"
MOTHER_VESSEL = "CONNECT VSL/VOY:"
STOWAGE_CODE = "STOWAGE CODE :"
FINAL_POD = "PORT OF DISCHARGING"
COMMODITY = "COMMODITY"
DISCHARGE_TERMINAL = "REMARKS"
CONTAINER_40HC = "40' HI-CUBE"
CONTAINER_40DV = "40' STANDARD DRY"
CONTAINER_20DV = "20' STANDARD DRY"


rect_booking_revised = (66, 0, 24, -7)
rect_date_booked = (36, 0, 120, -7)
rect_booking_number = (130, 2, 150, -7)
rect_departure_week = (130, 3, 250, -7)
rect_departure_date = (108, 3, 160, -7)
rect_discharge_port = (132, 3, 120, -7)
rect_mother_vessel = (48, 3, 400, -7)
rect_stowage_code = (84, 3, 100, -7)
rect_final_pod = (132, 3, 300, -7)
rect_commodity = (132, 3, 350, -7)
rect_discharge_terminal = (132, 3, 200, -7)
rect_container_hc = (-24, 10, -72, 0)
rect_container_dv = (-24, 10, -102, 0)
rect_container_weights = (100, 10, 150, -3)
rect_hazards = (400, 10, 500, -3)

ROOT_DIR = os.path.abspath('')
pdf_folder = r"bokningar_pdf\special"
file_dir = os.path.join(ROOT_DIR, pdf_folder)


def main(file_path):

    with open(file_path) as f:
        doc = fitz.open(f)
    
    total_height = 0.0
    total_words = []
    list_count_40hc, list_count_40dv, list_count_20dv = [], [], []
    list_tare_40hc, list_tare_40dv, list_tare_20dv = [], [], []
    list_nwt_40hc, list_nwt_40dv, list_nwt_20dv = [], [], []
    list_hazards_40hc, list_hazards_40dv, list_hazards_20dv = [], [], []
    
    for page in doc:
        word_list = page.get_text('words')
        for word in word_list:
            total_words.append([word[0], word[1] + total_height, word[2], word[3] + total_height, word[4]])
    
        d20 = page.search_for(CONTAINER_20DV)
        d40 = page.search_for(CONTAINER_40DV)
        h40 = page.search_for(CONTAINER_40HC)
    
        list_count_40hc.append(pf.get_container_amount(total_words, h40, rect_container_hc, total_height))
        list_count_40dv.append(pf.get_container_amount(total_words, d40, rect_container_dv, total_height))
        list_count_20dv.append(pf.get_container_amount(total_words, d20, rect_container_dv, total_height))
    
        list_nwt_40hc.append(pf.get_container_info(total_words, h40, rect_container_weights, total_height)[0])
        list_nwt_40dv.append(pf.get_container_info(total_words, d40, rect_container_weights, total_height)[0])
        list_nwt_20dv.append(pf.get_container_info(total_words, d20, rect_container_weights, total_height)[0])
    
        list_tare_40hc.append(pf.get_container_info(total_words, h40, rect_container_weights, total_height)[1])
        list_tare_40dv.append(pf.get_container_info(total_words, d40, rect_container_weights, total_height)[1])
        list_tare_20dv.append(pf.get_container_info(total_words, d20, rect_container_weights, total_height)[1])

        list_hazards_40hc.append(pf.get_container_hazards(total_words, h40, rect_hazards, total_height))
        list_hazards_40dv.append(pf.get_container_hazards(total_words, d40, rect_hazards, total_height))
        list_hazards_20dv.append(pf.get_container_hazards(total_words, d20, rect_hazards, total_height))

    
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
    

    """{'nwt': {'45G1': pf.calculate_weights(list_nwt_40hc, list_count_40hc),
                            '42G1': pf.calculate_weights(list_nwt_40dv, list_count_40dv),
                            '22G1': pf.calculate_weights(list_nwt_20dv, list_count_20dv)
                            },
                    'tare': {'45G1': pf.calculate_weights(list_tare_40hc, list_count_40hc),
                            '42G1': pf.calculate_weights(list_tare_40dv, list_count_40dv),
                            '22G1': pf.calculate_weights(list_tare_20dv, list_count_20dv)
                            },
                    'tonnes': {'45G1': pf.calculate_vgm(list_nwt_40hc, list_tare_40hc, list_count_40hc),
                               '42G1': pf.calculate_vgm(list_nwt_40dv, list_tare_40dv, list_count_40dv),
                               '22G1': pf.calculate_vgm(list_nwt_20dv, list_tare_20dv, list_count_20dv)}
                    },"""

    return_dict = {
        'filename': file,
        'booking_revised': booking_revised,
        'date_booked': pf.trim_date_string(date_booked),
        'same_date': pf.check_if_dates_match(date_booked, departure_date),
        'booking_number': booking_number,
        'departure_voy': departure_voy,
        'departure_week': pf.get_week(departure_date),
        'departure_date': departure_date,
        'discharge_port': discharge_port,
        'ocean_vessel': pf.ocean_vessel_and_voy(mother_vessel)['vessel'],
        'voyage': pf.ocean_vessel_and_voy(mother_vessel)['voy'],
        'stowage_code': stowage_code,
        'final_pod': pf.extract_final_pod(final_pod),
        'commodity': commodity,
        'discharge_terminal': discharge_terminal,   #endast "godkända" terminaler ska tas med
        'container_amount': {'45G1': pf.concatenate_floats(list_count_40hc),
                             '42G1': pf.concatenate_floats(list_count_40dv),
                             '22G1': pf.concatenate_floats(list_count_20dv)
                             },
        'weights': {'45G1': pf.calculate_vgm(list_nwt_40hc, list_tare_40hc, list_count_40hc),
                    '42G1': pf.calculate_vgm(list_nwt_40dv, list_tare_40dv, list_count_40dv),
                    '22G1': pf.calculate_vgm(list_nwt_20dv, list_tare_20dv, list_count_20dv)
                    },        

        'hazardous_cargo': {'45G1': pf.create_hazards_list(list_hazards_40hc),
                            '42G1': pf.create_hazards_list(list_hazards_40dv),
                            '22G1': pf.create_hazards_list(list_hazards_20dv)
                            }
    }
    return return_dict

if __name__ == '__main__':
    #for file in tqdm(os.listdir(file_dir)):
    for file in os.listdir(file_dir):
        for key, value in main(os.path.join(file_dir, file)).items():
            print(f'{key:>20}: {str(value)}')
        print("----------------------"*4)
    
