class MyJsonObject(dict):
    '''Returns ocr objects (docstring)
    (to show docstrings, "execute print(OcrObject.__dec__)")

    Args:
     - a

    Returns:
     - a
    
    '''
    # "->" は関数のアノテーション（返り値の型を注釈として記載できる）
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        """
        for arg in args:
            if isinstance(arg, dict):
                for k, v in arg.iteritems():
                    self[k] = v
        if kwargs:
            for k, v in kwargs.iteritems():
                self[k] = v
        """
    def __getattr__(self, attr):
        return self.get(attr)
    '''
    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    '''
    def __setitem__(self, key, value):
        # super().__setitem__(key, value)
        self.__dict__.update({key: value})

    '''
    def __delattr__(self, item):
        self.__delitem__(item)

    def __delitem__(self, key):
        super().__delitem__(key)
        del self.__dict__[key]
    '''
        

"""
class OcrObject(JsonData):
    '''
    |- fulltext
    |- paragraphs
        |- texts (list of str)
        |- confidentials (list of int)
        |- bound_boxs (list of list?)
            |- vertices (list)
                |- x
                |- y
    |- sentences
        |- texts (list of str)
        |- languages (list of )
        |- confidentials (avg of words)
        |- bound_boxs (lsit of list)
    |- words
        |- texts (list of str)
        |- languages (list of str) -> sometimes not appeared
        |- confidentials (list of int)
        |- bound_boxs (list of list?)
    '''
    def __init__(self, *args, **kwargs) -> None:
        #self.__dict__.update({'fullText': ''})
        super().__setitem__('fullText', '')
        super().__setitem__('paragraphs', {'texts': [], 'confidentials': [], 'bound_boxes': []})
        super().__setitem__('sentences', {'texts': [], 'confidentials': [], 'bound_boxes': [], 'languages': []})
        super().__setitem__('words', {'texts': [], 'confidentials': [], 'bound_boxes': [], 'languages': []})
        # self.fullText = ''
        # self.paragraphs = {'texts': [], 'confidentials': [], 'bound_boxes': []}
        # self.sentences = {'texts': [], 'confidentials': [], 'bound_boxes': [], 'languages': []}
        # self.words = {'texts': [], 'confidentials': [], 'bound_boxes': [], 'languages': []}

    def __getattr__(self, attr):
        return self.get(attr)
"""