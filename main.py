import os 
from tkinter import filedialog

from set_credentials import set_credentials
import toeic_text_converter

MODE_OCR_TTS = 0
MODE_TTS_ONLY = 1

# folder setting
input_folder = "input/QuestionSound"
intermed_folder = "intermediate"
output_folder = "output"

# set authentification key for Google API
set_credentials()

# toeic_converter = ToeicTextConverter()

# execute Part1 data
# インプットフォルダ・アウトプットフォルダを指定するだけ。
part1_folder = "Part1"
img_file = "10.jpg"
exec_mode = MODE_TTS_ONLY # MODE_OCR_TTS  MODE_TTS_ONLY
exec_part = 1

input_file = os.path.join(*[input_folder, part1_folder, img_file])
intermed_file =  os.path.join(*[intermed_folder, part1_folder, os.path.basename(input_file).replace(".jpg", ".txt")])
output_file = os.path.join(*[output_folder, part1_folder, os.path.basename(input_file).replace(".jpg", ".mp4")])

# OCR Part
if exec_mode == MODE_OCR_TTS:
    ocr_string, ocr_uncertain = toeic_text_converter.img_to_text(input_file, intermed_file)
elif exec_mode == MODE_TTS_ONLY:
    ocr_string = toeic_text_converter.read_mod_ocr_result(intermed_file)
    ocr_uncertain = False
else:
    print("OCR Error: different execution mode has been designated.")
    raise

# TTS Part
if not ocr_uncertain:
    print(ocr_string)
    toeic_text_converter.text_to_sound(ocr_string, output_file, exec_part)
