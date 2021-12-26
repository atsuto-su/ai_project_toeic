# ocr execution file
import os

from lib.vision.my_ocr import MyOcr
from lib.vision import create_schema

def exec_ocr(ocr_file) -> str:

    # create json schema if not exists
    schema_name = 'json_schema.json'
    if not os.path.isfile(schema_name):
        create_schema.create_ocr_out_schema(schema_name)

    # create OCR instance and execute OCR
    ocr = MyOcr(schema_name)
    ocr.set_ocr_data(ocr_file)

    # get google vision response and parsed ocr data
    return ocr.get_ocr_text()