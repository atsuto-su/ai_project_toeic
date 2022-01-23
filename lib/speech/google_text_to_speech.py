import os

from google.cloud import texttospeech
from google.cloud.texttospeech_v1.types.cloud_tts import AudioConfig

from .speech_const import *

class GoogleTextToSpeech:
    def __init__(self):
        self.language_code = ""
        self.voice_name = ""
        self.ssml_gender = ""
        self.speak_speed = DEFAULT_SPEAK_SPEED

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
        if speak_speed < MIN_SPEAK_SPEED:
            self.speak_speed = MIN_SPEAK_SPEED
        elif speak_speed > MAX_SPEAK_SPEED:
            self.speak_speed = MAX_SPEAK_SPEED
        else:
            self.speak_speed = speak_speed

    def synthesize_config(self):
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

        return voice, audio_config


    def synthesize_text(self, speak_text, out_file):

        # check outfile extension
        if os.path.splitext(out_file)[1] != ".mp3":
            raise Exception("wrong file extension: outfile extension must be mp3." + "\n" + "file path: " + out_file)

        client = texttospeech.TextToSpeechClient()
        input_text = texttospeech.SynthesisInput(text=speak_text)

        voice, audio_config = self.synthesize_config()

        response = client.synthesize_speech(
            request={"input": input_text, "voice": voice, "audio_config": audio_config}
        )

        # The response's audio_content is binary.
        with open(out_file, "wb") as out:
            out.write(response.audio_content)
    
    
    def ssml_to_audio(self, ssml_text, outfile):
        # Generates SSML text from plaintext.
        #
        # Given a string of SSML text and an output file name, this function
        # calls the Text-to-Speech API. The API returns a synthetic audio
        # version of the text, formatted according to the SSML commands. This
        # function saves the synthetic audio to the designated output file.
        #
        # Args:
        # ssml_text: string of SSML text
        # outfile: string name of file under which to save audio output
        #
        # Returns:
        # nothing

        # check outfile extension
        if os.path.splitext(outfile)[1] != ".mp3":
            raise Exception("wrong file extension: outfile extension must be mp3." + "\n" + "file path: " + outfile)

        # Instantiates a client
        client = texttospeech.TextToSpeechClient()

        # Sets the text input to be synthesized
        synthesis_input = texttospeech.SynthesisInput(ssml=ssml_text)

        # Builds the voice request, selects the language code and the SSML voice gender
        voice, audio_config = self.synthesize_config()

        # Performs the text-to-speech request on the text input with the selected
        # voice parameters and audio file type
        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

        # Writes the synthetic audio to the output file.
        with open(outfile, "wb") as out:
            out.write(response.audio_content)
            # print("Audio content written to file " + outfile)