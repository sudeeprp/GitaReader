import json
from translit import gita_to_devanagari

def mdtext(para_jsonstr):
    para = json.loads(para_jsonstr)
    return content_to_md(para['content'], para['style'])

def content_to_md(content, style):
    texts = [t['content'] for t in content if t['type'] == 'text']
    convert_to_md = stylemapper[style]
    return convert_to_md(texts[0])

stylemapper = {
    "normal": lambda x: x,
    "shloka": gita_to_devanagari,
    "heading1": lambda x: f'# {x}',
    "heading2": lambda x: f'## {x}'
}
