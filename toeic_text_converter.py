
import lib.speech.exec_my_tts as exec_my_tts
import lib.vision.exec_my_ocr as exec_my_ocr

class ToeicTextConverter():
    def __init__(self):
        pass

    def part1_conv(self, img_file, out_file, intermed_file=""):
        #input: image file
        #output: speech text (single speaker)
        img_text = exec_my_ocr.exec_ocr(img_file)
        if intermed_file:
            self.save_ocr_strings(img_text, intermed_file)
        exec_my_tts.single_speaker_tts(img_text, out_file)

    def part2_conv(self, img_file, out_file):
        self.part1_conv(img_file, out_file)

    def part3_conv(self, img_file, out_file):
        pass

    def part4_conv(self, img_file, out_file):
        pass
   
    def save_ocr_strings(self, ocr_string, file_name) -> None:
        with open(file_name, 'wt', encoding='utf-8') as f:
            f.write(ocr_string)
