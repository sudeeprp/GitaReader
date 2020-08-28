from copy import deepcopy
import json
import re
import gita_encode
import translit
from json import encoder


def write_head(dart_file):
    head_contents = '''
import 'contents.dart';
Contents gitaContents = Contents(ContentStructure('Chapter', 'Shloka', ''),
<GulpableUnit>[
'''
    dart_file.write(head_contents)


def write_tail(dart_file):
    tail_contents = ']'
    dart_file.write(tail_contents)


def blank_content():
    return {
        "devanagri": "",
        "shloka": "",
        "translation": [],
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
        joiner_text = '\n'
    return joiner_text


def fill_shlokahead_from_para(para, content):
    if "shloka" in para:
        content["book-keep"]["shlokahead"] = para["shloka"]
    return content


def fill_chapterhead_from_para(para, content):
    if "chapter" in para:
        content["book-keep"]["chapterhead"] = para["chapter"].replace('Chapter', 'Ch')
    return content


def filter_blanks(tokens):
    return [t for t in tokens if t]


def tokenize_translits(text_to_style):
    translits = []
    translation = {}
    tokens_in_xlat = re.split(r'(\[[^\[]+\])', text_to_style)
    for token in filter_blanks(tokens_in_xlat):
        if token.startswith('['):
            token = token[1:-1]
            translation['english'] = token
            translation['sanskrit'] = translit.gita_to_devanagari(token)
        else:
            translation['translate'] = token
            translits.append(translation)
            translation = {}
    return translits


def shloka_filler(element, content):
    text_in_shloka = element["content"]
    if len(text_in_shloka) > 1:     # to avoid the single "["
        content["shloka"] += delimiter_for_join(content["shloka"]) +\
                             text_in_shloka
        content["devanagri"] += delimiter_for_join(content["devanagri"]) +\
                               translit.gita_to_devanagari(text_in_shloka)
    return content


def translation_filler(element, content):
    content["translation"].extend(tokenize_translits(element["content"]))
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


def present_text(type, text):
    return f"  Presentable.text('{type}', {encoder.encode_basestring_ascii(text)}),\n"


def write_dart(oneshloka, dart_file):
    dart_file.write("GulpableUnit(\n")
    dart_file.write(f"<String>['{oneshloka['chapter']}', '{oneshloka['shloka']}'],\n")
    dart_file.write("Presentable.parent('shloka', <Presentable>[\n")
    dart_file.write("Presentable.parent('shlokaScript', <Presentable>[\n")
    dart_file.write(present_text('dvngr', oneshloka['content']['devanagri']))
    dart_file.write(present_text('ascii', oneshloka['content']['shloka']))
    dart_file.write("]),\n")
    dart_file.write("Presentable.parent('translation', <Presentable>[\n")
    for translation in oneshloka['content']['translation']:
        dart_file.write(present_text('english', translation['english']))
        dart_file.write(present_text('sanskrit', translation['sanskrit']))
        dart_file.write(present_text('translate', translation['translate']))
    dart_file.write("]),\n")
    dart_file.write("Presentable.parent('commentary', <Presentable>[\n")
    for insight_commentary in oneshloka['content']['insights']:
        dart_file.write(present_text('insight', insight_commentary[0]))
        dart_file.write(present_text('explanation', insight_commentary[1]))
    dart_file.write("]),\n")
    dart_file.write("]),\n")
    dart_file.write("),\n")


def extract_verses(docx_as_dict, dart_file):
    verses = []

    def add_to_verses(content):
        if len(content["shloka"]) > 0:
            content_to_write = deepcopy(content)
            del content_to_write["book-keep"]
            write_dart({
                "id": "*",
                "chapter": content["book-keep"]["chapterhead"],
                "shloka": content["book-keep"]["shlokahead"],
                "style": "shloka",
                "type": "text",
                "content": content_to_write
            }, dart_file)

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
    with open('verse.dart', 'w') as dart_file:
        write_head(dart_file)
        verse_json = extract_verses(docx_as_dict, dart_file)
        write_tail(dart_file)
