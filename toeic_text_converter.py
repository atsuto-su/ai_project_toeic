from lib.vision.my_ocr import MyOcr
# from lib.speech.google_text_to_speech import GoogleTextToSpeech
import lib.speech.exec_my_tts as exec_my_tts

class ToeicTextConverter():
    def __init__(self):
        pass

    def part1_conv(self, img_file, out_file, intermed_file="") -> None:
        #input: image file
        #output: speech text (single speaker)
        # img_text = exec_my_ocr.exec_ocr(img_file, intermed_file)

        # execute OCR
        ocr = MyOcr(img_file)
        ocr_string = ocr.get_ocr_text()

       # save ocr string if save file is set
        if intermed_file:
            ocr.save_ocr_text(intermed_file)

        # warning message if some ocr strings are uncertain.
        if ocr.uncertain_str_exist:
            print("uncertain ocr results exist.")

        else:
            # get google vision response and parsed ocr data
            exec_my_tts.single_speaker_tts(ocr_string, out_file)

    def part2_conv(self, img_file, out_file) -> None:
        self.part1_conv(img_file, out_file)

    def part3_conv(self, img_file, out_file) -> None:
        pass

    def part4_conv(self, img_file, out_file) -> None:
        pass