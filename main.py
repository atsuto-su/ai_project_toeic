import os 

from set_credentials import set_credentials
from toeic_text_converter import ToeicTextConverter

# folder setting
input_folder = "input/QuestionSound"
intermed_folder = "intermediate"
output_folder = "output"

# set authentification key for Google API
set_credentials()

toeic_converter = ToeicTextConverter()

# execute Part1 data
# インプットフォルダ・アウトプットフォルダを指定するだけ。
part1_folder = "Part1"
img_file = "01.jpg"

input_file = "/".join([input_folder, part1_folder, img_file])
intermed_file = "/".join([intermed_folder, part1_folder, os.path.basename(input_file).replace(".jpg", ".txt")])
output_file = "/".join([output_folder, part1_folder, os.path.basename(input_file).replace(".jpg", ".mp4")])

toeic_conv = ToeicTextConverter()
toeic_conv.part1_conv(input_file, output_file, intermed_file)