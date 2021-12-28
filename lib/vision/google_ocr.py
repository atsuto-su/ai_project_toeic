import io
import os
from google.auth import credentials

#Imports the Google Cloud client library
from google.cloud import vision
from PIL import Image, ImageDraw

class GoogleOcr():
    '''
        common process for google vision api (ocr)
    '''
    def __init__(self, ocr_file):
        self.ocr_response = ""
        self.set_ocr_response(ocr_file)

    def set_ocr_response(self, ocr_file) -> None:
        # Instantiates a client
        client = vision.ImageAnnotatorClient()
        # if you want to authenticate here, write as below
        # from google.oauth2 import service_account
        # credentials = service_account.Credentials.from_service_account_file(file_name)
        # client = vision.ImageAnnotatorClient(credentials=credentials)

        # The name of the image file to annotate
        ocr_file_path = os.path.abspath(ocr_file)

        # Loads the image into memory
        with io.open(ocr_file_path, 'rb') as image_file:
            content = image_file.read()

        image = vision.Image(content=content)

        response = client.document_text_detection(image=image)
        if response.error.message:
            raise Exception(
                '{}\nFor more info on error messages, check: '
                'https://cloud.google.com/apis/design/errors'.format(
                    response.error.message))
                
        self.ocr_response = response

    def get_ocr_response(self):
        return self.ocr_response

    def save_ocr_response(self, save_file) -> None:
        with open(save_file, 'wt', encoding='utf-8') as f:
            f.write(str(self.ocr_response))

    def draw_boxes(image, bounds, color) -> Image:
        """ Draw a border around the image using the hints in the vector list.
            bound in bounds = (x0,y0, x1,y1, x2,y2, x3,y3),
            0->up left, 1-> up right, 2->botton right, 3-> bottom left
        """
        draw = ImageDraw.Draw(image)

        for bound in bounds:
            draw.polygon([
                bound.vertices[0].x, bound.vertices[0].y,
                bound.vertices[1].x, bound.vertices[1].y,
                bound.vertices[2].x, bound.vertices[2].y,
                bound.vertices[3].x, bound.vertices[3].y], None, color)
        return image