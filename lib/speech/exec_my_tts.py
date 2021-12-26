import os
import ffmpeg
from lib.speech.google_text_to_speech import GoogleTextToSpeech
#from lib.speech.mp3_to_m4a import mp3_to_m4a

def single_speaker_tts(text_string, out_file, voice_type=0, speak_speed=1.0) -> None:
    speaker = GoogleTextToSpeech()
    speaker.set_speak_speed(speak_speed)
    speaker.set_voice_male(voice_type)
    speaker.synthesize_text(text_string, out_file)

"""
def multi_speakers_tts(list_text_strings, out_file, list_voice_types, speak_speed=1.0) -> None:
    dir_path = os.path.dirname(out_file)
    for text_string in list_text_strings:
        file_path = dir_path + "/" + "tmp.mp4"
        single_speaker_tts(text_string, file_path, speak_speed)
        
        # 作成したファイルをffmpegで結合する処理

    # for (name, age) in zip(name_list, age_list)


"""