from copy import deepcopy
import json
import re
import gita_encode
import translit


def blank_content():
    return {
        "devanagri": "",
        "shloka": "",
        "translation": "",
        "insights": [],
        "book-keep": {}
    }


def initial_content(init_material):
    initial = blank_content()
    initial.update(init_material)
    return initial


def init_blank_insight_if_empty(content):
    if len(content["insights"]) == 0:
        last_insight = ""
        if "lastinsight" in content["book-keep"]:
            last_insight = content["book-keep"]["lastinsight"]
        content["insights"] = [[last_insight, ""]]
    return content


def delimiter_for_join(previous_text):
    joiner_text = ""
    text_to_check = previous_text.strip()
    if len(text_to_check) > 0 and text_to_check[-1] in '.|।॥-':
        joiner_text = '<br>'
    return joiner_text


def fill_shlokahead_from_para(para, content):
    if "shloka" in para:
        content["book-keep"]["shlokahead"] = para["shloka"]
    return content


def fill_chapterhead_from_para(para, content):
    if "chapter" in para:
        content["book-keep"]["chapterhead"] = para["chapter"].replace('Chapter', 'Ch')
    return content


def span(style_name, readable):
    return f"<span class='{style_name}'>[{readable}]</span>"


def style_translits(text_to_style):
    styled = ''
    tokens_in_xlat = re.split(r'(\[[^\[]+\])', text_to_style)
    for token in tokens_in_xlat:
        if token.startswith('['):
            token = token[1:-1]
            token = span('transliteration', token) +\
                    span('sanskrit', translit.gita_to_devanagari(token))
        styled += token
    return styled


def shloka_filler(element, content):
    text_in_shloka = element["content"]
    if len(text_in_shloka) > 1:     # to avoid the single "["
        content["shloka"] += delimiter_for_join(content["shloka"]) +\
                             text_in_shloka
        content["devanagri"] += delimiter_for_join(content["devanagri"]) +\
                               translit.gita_to_devanagari(text_in_shloka)
    return content


def translation_filler(element, content):
    text_in_translation = delimiter_for_join(content["translation"])
    text_in_translation += style_translits(element["content"])
    content["translation"] += text_in_translation
    return content


def notes_filler(element, content):
    note = element["content"]
    content["book-keep"]["lastinsight"] = note
    content["insights"].append([note, ""])
    return content


def commentary_filler(element, content):
    content = init_blank_insight_if_empty(content)
    existing_commentary = content["insights"][-1][1]
    text_in_commentary = delimiter_for_join(existing_commentary)
    text_in_commentary += element["content"]
    content["insights"][-1][1] += text_in_commentary
    return content


FILLER_MAP = {
    "shloka": shloka_filler,
    "explnofshloka": translation_filler,
    "applnotes": notes_filler,
    "normal": commentary_filler
}


def form_presentable(paras, i, content):
    para_style = paras[i]['style']
    if para_style in FILLER_MAP:
        filler = FILLER_MAP[para_style]
        for element in paras[i]["content"]:
            content = filler(element, content)
    content = fill_shlokahead_from_para(paras[i], content)
    content = fill_chapterhead_from_para(paras[i], content)
    return content


def content_boundary(paras, i):
    found_boundary = False
    if i == len(paras) - 1:
        found_boundary = True
    elif paras[i+1]['shloka'] != paras[i]['shloka']:
        found_boundary = True
    return found_boundary


def extract_last_insight(content):
    return content["book-keep"]["lastinsight"]


def extract_verses(docx_as_dict):
    verses = []

    def add_to_verses(content):
        if len(content["shloka"]) > 0:
            content_to_write = deepcopy(content)
            del content_to_write["book-keep"]
            verses.append({
                "id": "*",
                "chapter": content["book-keep"]["chapterhead"],
                "shloka": content["book-keep"]["shlokahead"],
                "style": "shloka",
                "type": "text",
                "content": content_to_write
            })

    paras = docx_as_dict['paragraphs']
    content = blank_content()
    for i in range(len(paras)):
        content = form_presentable(paras, i, content)
        if content_boundary(paras, i):
            last_insight = extract_last_insight(content)
            add_to_verses(content)
            content = initial_content({"book-keep": {"lastinsight": last_insight}})
    return {"Verses": verses}


if __name__ == '__main__':
    docx_as_dict = gita_encode.encode_doc('GitaBhashya-try.docx')
    with open('verse.json', 'w') as verses_file:
        json.dump(extract_verses(docx_as_dict), verses_file, indent=2)
        print("Wrote the verses to verse.json")
