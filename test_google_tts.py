from lib.speech.google_text_to_speech import GoogleTextToSpeech
from lib.speech.mp3_to_m4a import mp3_to_m4a

from set_credentials import set_credentials


if __name__ == "__main__":

    folder = 'output/vision/'
    file_nameA = 'response_sentence01.txt'
    file_nameB = 'response_sentence10.txt'
    # read google vision ocr result
    with open(folder + file_nameA) as f:
        s1 = f.read()
    with open(folder + file_nameB) as f:
        s2 = f.read()

    # set authentification key
    set_credentials()

    out_folder = 'output/speech/'
    out_file = file_nameA.replace('.txt', '.mp3')
    out_file2 = file_nameB.replace('.txt', '.mp3')
    speakerA = GoogleTextToSpeech()
    speakerB = GoogleTextToSpeech()
    speakerA.set_voice_engb_female()
    speakerB.set_speak_fast()

    speakerA.synthesize_text(s1, out_folder + out_file)
    speakerB.synthesize_text(s2, out_folder + out_file2)

    # speakerA.mp3_to_m4a(out_file)