from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate


GITA_TO_HK = {
    "jn": 'jJ',
    "sh": 'z',
    "r`": 'R',
    "r'": 'R',
    ":": 'H',
    "Sh": 'S',
    "nkh": 'Gkh',
    "ng": 'Gg',
    "nk": 'Gk',
    "ch": 'c',
    "Ch": 'ch',
    "E": 'e',
    "O": 'o',
    "w": 'v',
    "_": "'"
}


def to_harward_kyoto(gita_transliteration):
    for gita_chars in GITA_TO_HK:
        gita_transliteration =\
            gita_transliteration.replace(gita_chars, GITA_TO_HK[gita_chars])
    return gita_transliteration


def to_devanagari(gita_transliteration):
    hk_translit = to_harward_kyoto(gita_transliteration)
    return transliterate(hk_translit, sanscript.HK, sanscript.DEVANAGARI)
