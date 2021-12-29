import os
from lib.vision.my_ocr import MyOcr
from lib.speech.my_text_to_speech import MyTextToSpeech
from lib.speech.speech_const import *

def img_to_text(input_file, save_file='') -> str:
    if os.path.splitext(input_file)[1] == ".jpg":
        # execute OCR
        ocr = MyOcr(input_file)
        ocr_string = ocr.get_ocr_text()

        # save ocr string if save file is set
        if save_file:
            ocr.save_ocr_text(save_file)

        # warning message if some ocr strings are uncertain.
        if ocr.uncertain_str_exist:
            print("Warning: uncertain ocr results exist.")
            ocr_uncertain = True

        return ocr_string, ocr_uncertain

    else:
        print("OCR Error: different file seems to be designated. File Extention must be jpg")
        raise

def read_mod_ocr_result(text_file) -> str:
    if os.path.splitext(text_file)[1] == ".txt":
        # read txt file
        with open(text_file, 'r', encoding='utf-8') as f:
            read_text = f.read()

        return read_text

    else:
        print("OCR Error: different file seems to be designated. File Extention must be txt")
        raise

def text_to_sound(ocr_string, out_file, exec_part) -> None:
    # tts part
    if exec_part == 1:
        speaker = MyTextToSpeech(
                    set_female=True, 
                    voice_type=VOICE_TYPE_US, 
                    speak_speed=NORMAL_SPEAK_SPEED
                    )
        speaker.synthesize_text(ocr_string, out_file)

    elif exec_part == 2:
        pass
    elif exec_part == 3:
        pass
    elif exec_part == 4:
        pass
    else:
        print("Error: Undefined execution part has been designated.")


# def part1_conv(img_file, out_file, save_file="") -> None:
#     '''
#         input: image file
#         output: speech text (single speaker)
#     '''
#     # execute OCR
#     ocr = MyOcr(img_file)
#     ocr_string = ocr.get_ocr_text()

#     # save ocr string if save file is set
#     if save_file:
#         ocr.save_ocr_text(save_file)

#     # warning message if some ocr strings are uncertain.
#     if ocr.uncertain_str_exist:
#         print("uncertain ocr results exist.")

#     else:
#         # execute tts
#         speaker = MyTextToSpeech(
#                     set_female=True, 
#                     voice_type=VOICE_TYPE_US, 
#                     speak_speed=NORMAL_SPEAK_SPEED
#                     )
#         speaker.synthesize_text(ocr_string, out_file)

# def part2_conv(self, img_file, out_file) -> None:
#     self.part1_conv(img_file, out_file)

# def part3_conv(self, img_file, out_file) -> None:
#     pass

# def part4_conv(self, img_file, out_file) -> None:
#     pass