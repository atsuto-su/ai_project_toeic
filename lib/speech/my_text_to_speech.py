import ffmpeg

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

