def get_value(value):
    return None if value == '\N' else value.lower().strip()

def get_language(value):
    languages = {'eng': 1, 'spa': 2, 'por': 3, 'fra': 4}
    try:
        lang = get_value(value) and languages[get_value(value)] or 0
    except KeyError:
        lang = 0
    return lang

def get_transportation(value):
    transportations = {'plane': 1, 'bus': 2, 'car': 3, 'train': 4}
    try:
        transport = get_value(value) and transportations[get_value(value)] or 0
    except KeyError:
        transport = 1
    return transport


