from dataclasses import dataclass

import fitz

file_path= r'bokningar_pdf\SB0LQTPC.PDF'

with open(file_path) as f:
        doc = fitz.open(f)

"/ REVISE :"
"DATE:"
"BOOKING NO."
"VESSEL/VOYAGE"
"ETD DATE"
"T/S PORT"
"VSL/VOY:"
"""STOWAGE CODE"""
"PORT OF DISCHARGING"
"COMMODITY"
"REMARKS"
"QTY/TYPE"
"GWT+TARE"
"WT(KGS)"
"IMO CLASS/UN"

@dataclass
class BookingRevised:
        pass

@dataclass
class DateBooked:
        pass

@dataclass
class BookingNumber:
        pass

@dataclass
class DepartureWeek:
        pass

@dataclass
class DepartureDate:
        pass

@dataclass
class DischargePort:
        pass

@dataclass
class MotherVessel:
        pass

@dataclass
class FinalPod:
        pass

@dataclass
class Commodity:
        pass

@dataclass
class DischargeTerminal:
        pass

@dataclass
class ContainerInfo:
        pass

@dataclass
class ContainerWeight:
        pass

@dataclass
class ContainerTare:
        pass

@dataclass
class DangerousCargo:
        pass