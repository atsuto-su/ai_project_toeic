import os
import json
import traceback
import datetime

#Imports the Google Cloud client library
# from lib.vision.google_ocr import GoogleOcr
# from lib.vision.my_json_object import MyJsonObject
from .google_ocr import GoogleOcr
from .my_json_object import MyJsonObject

class MyOcr(GoogleOcr):
    ##########################
    # initialization #
    ##########################
    def __init__(self, ocr_file) -> None:
        self.response = ""
        self.ocr_data = ""
        self.ocr_text = ""
        self.failed_str_exist = False
        self.uncertain_str_exist = False

        self.init_ocr_data()
        self.set_ocr_data(ocr_file)
        self.set_ocr_text()

    def init_ocr_data(self) -> None:
        # create json schema if not exists
        schema_file = os.path.join(os.path.dirname(__file__), 'json_schema.json')
        if not os.path.isfile(schema_file):
            self.set_ocr_data_schema(schema_file)

        # initialize ocr data with MyJsonObject schema
        with open(schema_file, mode='rt', encoding='utf-8') as f:
            self.ocr_data = json.load(f, object_hook=MyJsonObject)


    def set_ocr_data_schema(self, schema_file) -> None:
        ### TBM: want to change so that json-file becomes unnecessary ###
        schema_dic = {
            "fullText": "",
            "paragraphs": {
                "texts": [],
                # "confidences": [],
                "bounding_boxes": []
            },
            "sentences": {
                "texts": [],
                # "confidences": [],
                "bounding_boxes": [],
                # "languages": []
            },
            "words": {
                "texts": [],
                "confidences": [],
                "bounding_boxes": [],
                "languages": []
            },
            "warning_words_boundings": [],
            "failed_words_boundings": []
        }
        # t: text mode
        with open(schema_file, mode='wt', encoding='utf-8') as f:
            json.dump(schema_dic, f, ensure_ascii=False, indent=4)


    ##########################
    # setter #
    ##########################
    def set_ocr_data(self, ocr_file) -> None:
        '''Returns orc results as json-formed dictionary
        Args:
        - file_name (str)
        '''
        # constants
        CONF_ERR_BORDER = 0.3
        CONF_WARNING_BORDER = 0.7
        WARNING_STRING = '(*)'

        self.set_ocr_response(ocr_file)

        # assign ocr results to schema
        self.ocr_data.fullText = self.ocr_response.text_annotations[0].description

        # pages > blocks > paragraphs > words > symbols
        full_annotation = self.ocr_response.full_text_annotation

        try:
            for page in full_annotation.pages:
                for block in page.blocks:
                    for paragraph in block.paragraphs:
                        paragraph_tmp = ''
                        sentence_tmp = ''
                        for word in paragraph.words:
                            word_tmp = ''
                            for symbol in word.symbols:
                                word_tmp += symbol.text
                                if symbol.property.detected_break:
                                    str_detected_break = str(symbol.property.detected_break.type_)
                                    # print("word: " + word_tmp + ", detected_break: " + str_detected_break)
                                else:
                                    str_detected_break = ''
                            # delete/mark the word according to its confidence
                            if word.confidence <= CONF_ERR_BORDER:
                                ### NOTE empty is okay? ###
                                word_tmp = ''
                                self.ocr_data.failed_words_boundings.append(word.bounding_box)
                                self.failed_str_exist = True
                            elif word.confidence <= CONF_WARNING_BORDER:
                                word_tmp += WARNING_STRING
                                self.ocr_data.warning_words_boundings.append(word.bounding_box)
                                self.uncertain_str_exist = True
                                # print("ocr uncertain: " + word_tmp)
                            # assign words data
                            self.ocr_data.words.texts.append(word_tmp)
                            self.ocr_data.words.confidences.append(word.confidence)
                            self.ocr_data.words.bounding_boxes.append(word.bounding_box)
                            if word.property.detected_languages == []:
                                word_language = ''
                            else:
                                word_language = word.property.detected_languages[0].language_code
                            self.ocr_data.words.languages.append(word_language)

                            # assign sentence data
                            sentence_tmp += word_tmp

                            # paragraph跨ぎになっているので、修正必要
                            if word_tmp.strip(WARNING_STRING)[-1:] in ['.', '?']:
                                self.ocr_data.sentences.texts.append(sentence_tmp)
                                paragraph_tmp += sentence_tmp + '\n'
                                sentence_tmp = ''
                            else:
                                if any(s in str_detected_break for s in ['.SPACE', '.SURE_SPACE', '.EOL_SURE_SPACE', '.LINE_BREAK']):
                                    sentence_tmp += ' '
                                elif any(s in str_detected_break for s in ['.HYPHEN', '']):
                                    sentence_tmp += ''
                                else:
                                    sentence_tmp += '_'
                        if sentence_tmp not in self.ocr_data.sentences.texts:
                            self.ocr_data.sentences.texts.append(sentence_tmp)

                        # assign paragraph data
                        self.ocr_data.paragraphs.texts.append(paragraph_tmp)
                        self.ocr_data.paragraphs.bounding_boxes.append(paragraph.bounding_box)
        except:
            now = datetime.datetime.now()
            str_now = now.strftime('%Y%m%d-%H%M%S')
            log_folder = './log/'
            # write ocr response into file
            self.output_ocr_response(f'{log_folder}response_{str_now}.txt')
            # write error contents into log file
            with open(f'{log_folder}error_{str_now}.log', 'w') as f:
                traceback.print_exc(file=f)
            # re rase the error
            raise

    def set_ocr_text(self) -> None:
        self.ocr_text = '\n'.join(self.ocr_data.sentences.texts)


    ##########################
    # getter #
    ##########################
    def get_ocr_data(self) -> MyJsonObject:
        return self.ocr_data

    def get_ocr_text(self) -> str:
        return self.ocr_text


    ##########################
    # save method #
    ##########################
    def save_word_data(self, save_file) -> None:
        with open(save_file, 'wt', encoding='utf-8') as f: 
            for index, _ in enumerate(self.ocr_data.words.texts):
                f.write(self.ocr_data.words.texts[index] + ",")
                f.write(str(self.ocr_data.words.confidences[index]) + ",")
                f.write(str(self.ocr_data.words.bounding_boxes[index]) + ",")
                f.write(str(self.ocr_data.words.languages[index]) + "\n---------------------\n") 

    def save_sentence_data(self, save_file) -> None:
        with open(save_file, 'wt', encoding='utf-8') as f:
            f.write('\n'.join(self.ocr_data.sentences.texts))

    def save_paragraph_data(self, save_file) -> None:
        with open(save_file, 'wt', encoding='utf-8') as f:
            f.write('\n\n'.join(self.ocr_data.paragraphs.texts))

    def save_ocr_text(self, save_file) -> None:
        with open(save_file, 'wt', encoding='utf-8') as f:
            f.write(self.ocr_text)
