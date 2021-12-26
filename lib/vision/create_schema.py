import json

def create_ocr_out_schema(filename, dir="./") -> None:
    json_dic = {
        "fullText": "",
        "paragraphs": {
            "texts": [],
            "confidences": [],
            "bounding_boxes": []
        },
        "sentences": {
            "texts": [],
            "confidences": [],
            "bounding_boxes": [],
            "languages": []
        },
        "words": {
            "texts": [],
            "confidences": [],
            "bounding_boxes": [],
            "languages": []
        }
    }
    # t: text mode
    with open(dir+filename, mode='wt', encoding='utf-8') as f:
        json.dump(json_dic, f, ensure_ascii=False, indent=4)
