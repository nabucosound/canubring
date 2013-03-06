def get_value(value):
    return None if value == '\N' else value.lower().strip()

def get_language(value):
    languages = {'eng': 1, 'spa': 2, 'por': 3, 'fra': 4}
    try:
        lang = get_value(value) and languages[get_value(value)] or 0
    except KeyError:
        lang = 0
    return lang


