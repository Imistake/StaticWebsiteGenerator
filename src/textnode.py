from enum import Enum

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        if isinstance(text_type, TextType):
            normalized = text_type
        elif isinstance(text_type, str):
            normalized = TextType(text_type)
        else:
            raise TypeError("text_type must be a TextType or valid string value")
        self.text_type = normalized
        self.url = url

    def __eq__(self, value):
        if isinstance(value, TextNode):
            return self.text == value.text and self.text_type == value.text_type and self.url == value.url 
        else:
            return False
        
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"