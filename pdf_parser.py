import fitz

file_path= r'bokningar_pdf\SB0LQTPC.PDF'

with open(file_path) as f:
        doc = fitz.open(f)

