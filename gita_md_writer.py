import json
from translit import gita_to_devanagari

def mdcumulate(para_sequence):
  chapters = {}
  def cumulate(chaptitle, para_md):
    if chaptitle not in chapters:
      chapters[chaptitle] = ''
    chapters[chaptitle] += para_md + '\n'

  para_groups = groupadja(para_sequence)
  for group in para_groups:
    cumulate(group['paras'][0]['chapter'], mdtext(group))
  return chapters

def groupadja(para_sequence):
  para_groups = [{"style": para_sequence[0]["style"], "paras": [para_sequence[0]]}]
  for next, para in zip(para_sequence[1:], para_sequence):
    if next["style"] == para["style"]:
      para_groups[-1]["paras"].append(next)
    else:
      para_groups.append({"style": next["style"], "paras": [next]})
  return para_groups

def mdtext(group):
  md = ''
  for para in group["paras"]:
    md += content_to_md(para['content'], group['style'])
    md += '\n'
  return md

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
