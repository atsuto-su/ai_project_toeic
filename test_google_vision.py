# Google Vision API Test
import os

from lib.vision.my_ocr import MyOcr
from lib.vision import create_schema

from set_credentials import set_credentials

# main start #
if __name__ == "__main__":
    folder_path = 'input/QuestionSound/Part3/'
    file_name = '65.jpg'
    file_path = folder_path + file_name

    # create json schema if not exists
    schema_name = 'json_schema.json'
    if not os.path.isfile(schema_name):
        create_schema.create_ocr_out_schema(schema_name)

    # set authentification key for Google API
    set_credentials()

    # create OCR instance and execute OCR
    ocr = MyOcr(schema_name)
    ocr.set_ocr_data(file_path)

    # get google vision response and parsed ocr data
    ocr_data = ocr.get_ocr_data()

    # write ocr results for analysis
    folder = 'output/vision/'
    ocr.output_ocr_response(folder + 'response_' + file_name.split('.')[0] + '.txt')
    ocr.output_word_data(folder + 'response_word_' + file_name.split('.')[0] +'_mod.txt')
    ocr.output_sentence_data(folder + 'response_sentence_' + file_name.split('.')[0] +'_mod.txt')
    ocr.output_paragraph_data(folder + 'response_paragraph_' + file_name.split('.')[0] +'_mod.txt')
 

