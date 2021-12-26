
import lib.speech.exec_my_tts as exec_my_tts
import lib.vision.exec_my_ocr as exec_my_ocr

class ToeicTextConverter():
    def __init__(self):
        pass

    def part1_conv(self, img_file, out_file):
        #input: image file
        #output: speech text (single speaker)
        img_text = exec_my_ocr.exec_ocr(img_file)
        exec_my_tts.single_speaker_tts(img_text, out_file)
        pass

    def part2_conv(self, img_file, out_file):
        self.part1_conv(img_file, out_file)
        pass

    def part3_conv(self, img_file, out_file):
        pass

    def part4_conv(self, img_file, out_file):
        pass
   