import ffmpeg
import html
import re

from .speech_const import *
from .google_text_to_speech import GoogleTextToSpeech

class MyTextToSpeech(GoogleTextToSpeech):

    def __init__(self, set_female, voice_type, speak_speed):
        super().__init__()
        # set voice
        self.set_voice(set_female, voice_type)
        # set normal speed
        self.set_speak_speed(speak_speed)

    def set_voice(self, set_female, voice_type):
        if set_female:
            self.set_voice_female(voice_type)
        else:
            self.set_voice_male(voice_type)

    def set_voice_male(self, voice_type=0):
        if voice_type == VOICE_TYPE_US:
            super().set_voice_enus_male()
        elif voice_type == VOICE_TYPE_GB:
            super().set_voice_engb_male()
        else: 
            print("Error: undefined voice type has been designated.")
            raise
    
    def set_voice_female(self, voice_type=0):
        if voice_type == VOICE_TYPE_US:
            super().set_voice_enus_female()
        elif voice_type == VOICE_TYPE_GB:
            super().set_voice_engb_female()
        else:
            print("Error: undefined voice type has been designated.")
            raise
 
    def mp3_to_m4a(mp3_file):
        # this function is necessary when you want to send voice data in LINE bot. (only m4a is compatible)
        '''
            reference:
            - https://pypi.org/project/ffmpeg-python/
            - https://qiita.com/satoshi2nd/items/4f6814b795a772af4af0
            - https://self-development.info/ffmpeg-python%E3%81%AB%E3%82%88%E3%82%8Awav%E3%82%92mp3%E3%81%AB%E5%A4%89%E6%8F%9B%E3%81%99%E3%82%8B%E3%80%90python%E3%80%91/
        '''
        stream = ffmpeg.input(mp3_file)
        stream = ffmpeg.output(stream, mp3_file.replace(".mp3", ".m4a"))
        ffmpeg.run(stream)

    def text_to_ssml(self, text, breaktime=0):
        # Convert plaintext to SSML
        ssml = '<speak>{}</speak>'.format(
            html.escape(text)
        )

        # Wait designated seconds between each address
        if breaktime != 0:
            ssml = ssml.replace('\n', '\n<break time="' + str(breaktime) + 's"/>')

        # Define enumerated items as characters
        for enum_mark in ENUM_MARKERS:
            if enum_mark in ssml:
                ssml = ssml.replace(enum_mark, 
                            '<say-as interpret-as="characters">'
                                + re.sub("[()]", "", enum_mark) + 
                            '</say-as>' + "!" +
                        '<break time="' + str(ENUM_BREAK) + 's"/>'
                        )

        # Return the concatenated string of ssml script
        return ssml
    
    # change voice: <voice language="en-GB" gender="male" required="gender"> ~~~ </ voice>

    def synthesize_text(self, speak_text, out_file, ssml_syn=False, breaktime=0):
        if ssml_syn:
            ssml_text = self.text_to_ssml(speak_text, breaktime)
            print(ssml_text)
            self.ssml_to_audio(ssml_text, out_file)
        else:
            super().synthesize_text(speak_text, out_file)
