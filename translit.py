import re
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


def gita_to_devanagari(gita_transliteration):
    hk_translit = to_harward_kyoto(gita_transliteration)
    devanagari = transliterate(hk_translit, sanscript.HK, sanscript.DEVANAGARI)
    if re.search(r'[\x22-\x2C\x2E-\x7F]+', devanagari): # ctrl-chars, space, !, - allowed
        print(f"WARNING: {gita_transliteration} translated to {devanagari}")
    return devanagari