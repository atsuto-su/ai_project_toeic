import os
import ffmpeg

from google.cloud import texttospeech

class GoogleTextToSpeech:

    MAX_SPEAK_SPEED = 1.5
    MIN_SPEAK_SPEED = 0.25  

    def __init__(self, speed=1.0):
        # set default voice
        self.set_voice_enus_male()
        # set normal speed
        self.set_speak_speed(speed)

        self.language_code = ""
        self.voice_name = ""
        self.ssml_gender = ""

    # for more options of voices, see https://cloud.google.com/text-to-speech/docs/voices?hl=ja
    def set_voice_enus_male(self):
        self.language_code = "en-US"
        self.voice_name="en-US-Standard-J"
        self.ssml_gender=texttospeech.SsmlVoiceGender.MALE

    def set_voice_enus_female(self):
        self.language_code = "en-US"
        self.voice_name="en-US-Standard-F"
        self.ssml_gender=texttospeech.SsmlVoiceGender.FEMALE

    def set_voice_engb_male(self):
        self.language_code = "en-GB"
        self.voice_name="en-GB-Wavenet-D"
        self.ssml_gender=texttospeech.SsmlVoiceGender.MALE

    def set_voice_engb_female(self):
        self.language_code = "en-GB"
        self.voice_name="en-GB-Wavenet-F"
        self.ssml_gender=texttospeech.SsmlVoiceGender.FEMALE

    def set_voice_male(self, voice_type=0):
        if voice_type == 0:
            self.set_voice_enus_male()
        else:
            self.set_voice_engb_male()
    
    def set_voice_female(self, voice_type=0):
        if voice_type == 0:
            self.set_voice_enus_female()
        else:
            self.set_voice_engb_female()

    def set_speak_fast(self):
        self.speak_speed = 1.5

    def set_speak_speed(self, speak_speed):
        if speak_speed < GoogleTextToSpeech.MIN_SPEAK_SPEED:
            self.speak_speed = GoogleTextToSpeech.MIN_SPEAK_SPEED
        elif speak_speed > GoogleTextToSpeech.MAX_SPEAK_SPEED:
            self.speak_speed = GoogleTextToSpeech.MAX_SPEAK_SPEED
        else:
            self.speak_speed = speak_speed

    def synthesize_text(self, text, outfile):

        # check outfile extension
        if os.path.splitext(outfile)[1] != ".mp4":
            raise Exception("wrong file extension: outfile extension must be mp4." + "\n" + "file path: " + outfile)

        client = texttospeech.TextToSpeechClient()
        input_text = texttospeech.SynthesisInput(text=text)

        # Note: the voice can also be specified by name.
        # Names of voices can be retrieved with client.list_voices().
        # refer to https://cloud.google.com/text-to-speech/docs/voices?hl=ja for details.
        voice = texttospeech.VoiceSelectionParams(
            language_code = self.language_code,
            name = self.voice_name,
            ssml_gender = self.ssml_gender
        )

        audio_config = texttospeech.AudioConfig(
            audio_encoding = texttospeech.AudioEncoding.MP3, # note: LINE bot Messaging API supports only M4A.
            speaking_rate = self.speak_speed # default=1.0, range in [0.25, 4.0]. 1.5 is realistically maximum.
        )

        response = client.synthesize_speech(
            request={"input": input_text, "voice": voice, "audio_config": audio_config}
        )

       # The response's audio_content is binary.
        with open(outfile, "wb") as out:
            out.write(response.audio_content)
    
    # def ssml_to_text():
        # see below link for how to insert pause into voice data
        # https://stackoverflow.com/questions/59819936/adding-a-pause-in-google-text-to-speech

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

