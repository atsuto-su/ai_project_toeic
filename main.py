import os 

from set_credentials import set_credentials
from toeic_text_converter import ToeicTextConverter


# folder setting
input_folder = "input/QuestionSound"
output_folder = "output"



# set authentification key for Google API
set_credentials()

toeic_converter = ToeicTextConverter()

# execute Part1 data
# インプットフォルダ・アウトプットフォルダを指定するだけ。
input_part1 = "input/QuestionSound/Part1"
output_part1 = "output/Part1"

input_file = input_part1 + "/" + "10.jpg"
output_file = output_part1 + "/" + os.path.basename(input_file).replace(".jpg", ".mp4")

toeic_conv = ToeicTextConverter()
toeic_conv.part1_conv(input_file, output_file)