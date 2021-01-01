import json
from translit import gita_to_devanagari

def mdcumulate(para_sequence):
  chapters = {}
  def cumulate(chaptitle, paramd):
    if chaptitle not in chapters:
      chapters[chaptitle] = ''
    chapters[chaptitle] += paramd + '\n'
  for para in para_sequence:
    cumulate(para['chapter'], mdtext(para))
  return chapters

def mdtext(para):
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
