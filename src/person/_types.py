import enum 


class Voice(enum.Enum):
    FILIPP = "filipp"
    ZAHAR = "zahar"
    MADIRUS = "madirus"


class TextModel(enum.Enum):
    LARGE = "gpt-3.5-turbo"
    SMALL = "text-embedding-3-small"