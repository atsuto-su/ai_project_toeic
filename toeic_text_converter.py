from lib.vision.my_ocr import MyOcr
from lib.speech.my_text_to_speech import MyTextToSpeech

class ToeicTextConverter():

    FAST_SPEAK_SPEED = 1.5
    NORMAL_SPEAK_SPEED = 1.0
    SLOW_SPEAK_SPEED = 0.5

    VOICE_TYPE_US = 0
    VOICE_TYPE_GB = 1

    def __init__(self):
        pass

    def part1_conv(self, img_file, out_file, intermed_file="") -> None:
        '''
            input: image file
            output: speech text (single speaker)
        '''
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
            # execute tts
            speaker = MyTextToSpeech(
                        set_female=True, 
                        voice_type=ToeicTextConverter.VOICE_TYPE_US, 
                        speak_speed=ToeicTextConverter.NORMAL_SPEAK_SPEED
                     )
            speaker.synthesize_text(ocr_string, out_file)

    def part2_conv(self, img_file, out_file) -> None:
        self.part1_conv(img_file, out_file)

    def part3_conv(self, img_file, out_file) -> None:
        pass

    def part4_conv(self, img_file, out_file) -> None:
        pass