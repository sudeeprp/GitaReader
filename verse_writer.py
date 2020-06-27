from copy import deepcopy
import json
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


def init_blank_insight_if_empty(content):
    if len(content["insights"]) == 0:
        content["insights"] = [["", ""]]
    return content


def joiner(previous_text):
    joiner_text = ""
    if previous_text.strip().endswith('.'):
        joiner_text = '<br>'
    return joiner_text


def shloka_filler(element, content):
    text_in_shloka = element["content"]
    if len(text_in_shloka) > 1:
        content["shloka"] += text_in_shloka + '<br>'
        content["devanagri"] = translit.to_devanagari(content["shloka"])
    return content


def translation_filler(element, content):
    text_in_translation = joiner(content["translation"])
    text_in_translation += element["content"]
    text_in_translation = text_in_translation.replace('[', "<span class='transliteration'>[")
    text_in_translation = text_in_translation.replace(']', "]</span>")
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
    text_in_commentary = joiner(existing_commentary)
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
    content["book-keep"]["shlokahead"] = paras[i]["shloka"]
    return content


def content_boundary(paras, i):
    found_boundary = False
    if i == len(paras) - 1:
        found_boundary = True
    elif paras[i+1]['shloka'] != paras[i]['shloka']:
        found_boundary = True
    return found_boundary


def extract_verses(docx_as_dict):
    verses = []

    def add_to_verses(content):
        if len(content["shloka"]) > 0:
            verses.append({
                "id": "*",
                "chapter": "Chapter *",
                "shloka": content["book-keep"]["shlokahead"],
                "style": "shloka",
                "type": "text",
                "content": deepcopy(content)
            })

    paras = docx_as_dict['paragraphs']
    content = blank_content()
    for i in range(len(paras)):
        content = form_presentable(paras, i, content)
        if content_boundary(paras, i):
            add_to_verses(content)
            content = blank_content()
    return {"Verses": verses}


if __name__ == '__main__':
    docx_as_dict = gita_encode.encode_doc('GitaBhashya-try.docx')
    with open('verse.json', 'w') as verses_file:
        json.dump(extract_verses(docx_as_dict), verses_file, indent=2)
        print("Wrote the verses to verse.json")
