import json
import traceback
import datetime

#Imports the Google Cloud client library
from lib.google_ocr import GoogleOcr
from lib.my_json_object import MyJsonObject

class MyOcr(GoogleOcr):
    def __init__(self, schema_file) -> None:
        self.init_ocr_data(schema_file)

    def init_ocr_data(self, schema_file) -> None:
       # initialize ocr data with MyJsonObject schema
        with open(schema_file, mode='rt', encoding='utf-8') as f:
            self.ocr_data = json.load(f, object_hook=MyJsonObject)

    def set_ocr_data(self, file_name) -> None:
        '''Returns orc results as json-formed dictionary
        Args:
        - file_name (str)
        '''
        # constants
        CONF_ERR_BORDER = 0.3
        CONF_WARNING_BORDER = 0.7
        WARNING_STRING = '{}(*)'

        self.set_ocr_response(file_name)

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
                                word_tmp = ''
                                self.ocr_data.failed_words_boundings.append(word.bounding_box)
                            elif word.confidence <= CONF_WARNING_BORDER:
                                word_tmp = WARNING_STRING.format(word_tmp)
                                self.ocr_data.warning_words_boundings.append(word.bounding_box)

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
                            if word_tmp[-1:] in ['.', '?']:
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

                            '''
                            if any(s in str_detected_break for s in ['.SPACE', '.SURE_SPACE']):
                                sentence_tmp += ' '
                            elif any(s in str_detected_break for s in ['.EOL_SURE_SPACE', '.LINE_BREAK']):
                                self.ocr_data.sentences.texts.append(sentence_tmp)
                                paragraph_tmp += sentence_tmp + '\n'
                                sentence_tmp = ''
                            elif any(s in str_detected_break for s in ['.HYPHEN', '']):
                                sentence_tmp += ''
                            else: 
                                sentence_tmp += '_'
                            '''
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

    def get_ocr_data(self) -> MyJsonObject:
        return self.ocr_data

    def output_word_data(self, file_name) -> None:
        with open(file_name, 'wt', encoding='utf-8') as f: 
            for index, _ in enumerate(self.ocr_data.words.texts):
                f.write(self.ocr_data.words.texts[index] + ",")
                f.write(str(self.ocr_data.words.confidences[index]) + ",")
                f.write(str(self.ocr_data.words.bounding_boxes[index]) + ",")
                f.write(str(self.ocr_data.words.languages[index]) + "\n---------------------\n") 

    def output_sentence_data(self, file_name) -> None:
        with open(file_name, 'wt', encoding='utf-8') as f:
            f.write('\n'.join(self.ocr_data.sentences.texts))

    def output_paragraph_data(self, file_name) -> None:
        with open(file_name, 'wt', encoding='utf-8') as f:
            f.write('\n\n'.join(self.ocr_data.paragraphs.texts))