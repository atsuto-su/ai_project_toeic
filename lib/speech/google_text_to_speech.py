import os
from google.cloud import texttospeech

class GoogleTextToSpeech:

    MAX_SPEAK_SPEED = 1.5
    MIN_SPEAK_SPEED = 0.25  
    DEFAULT_SPEAK_SPEED = 1.0

    def __init__(self):
        self.language_code = ""
        self.voice_name = ""
        self.ssml_gender = ""
        self.speak_speed = GoogleTextToSpeech.DEFAULT_SPEAK_SPEED

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

    def set_speak_speed(self, speak_speed):
        if speak_speed < GoogleTextToSpeech.MIN_SPEAK_SPEED:
            self.speak_speed = GoogleTextToSpeech.MIN_SPEAK_SPEED
        elif speak_speed > GoogleTextToSpeech.MAX_SPEAK_SPEED:
            self.speak_speed = GoogleTextToSpeech.MAX_SPEAK_SPEED
        else:
            self.speak_speed = speak_speed

    def synthesize_text(self, speak_text, out_file):

        # check outfile extension
        if os.path.splitext(out_file)[1] != ".mp4":
            raise Exception("wrong file extension: outfile extension must be mp4." + "\n" + "file path: " + out_file)

        client = texttospeech.TextToSpeechClient()
        input_text = texttospeech.SynthesisInput(text=speak_text)

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
        with open(out_file, "wb") as out:
            out.write(response.audio_content)
    
    # def ssml_to_text():
        # see below link for how to insert pause into voice data
        # https://stackoverflow.com/questions/59819936/adding-a-pause-in-google-text-to-speech

