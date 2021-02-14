import json
from contents2md import shlokaline_to_md, expln_to_meanings

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
  md_texts = [content_to_md(para['content'], group['style'])
    for para in group["paras"]]
  return compose_mds(md_texts, group['style'])

def content_to_md(content, style):
  texts = [t['content'] for t in content if t['type'] == 'text']
  try:
    convert_to_md = style2mdtext[style]
    return convert_to_md(texts[0])
  except KeyError:
    return ''

def compose_mds(md_texts, style):
  if style in stylecomposer:
    composer = stylecomposer[style]
  else:
    composer = stylecomposer[".default"]
  return composer(md_texts)

def compose_with_newlines(md_texts):
  return '\n'.join(md_texts)

def compose_with_newlines_and_a_gap(md_texts):
  return compose_with_newlines(md_texts) + '\n'

style2mdtext = {
  "normal": lambda text: text,
  "shloka": shlokaline_to_md,
  "heading1": lambda text: f'# {text}',
  "heading2": lambda text: f'## {text}',
  "explnofshloka": expln_to_meanings
}

stylecomposer = {
  ".default": compose_with_newlines,
  "heading1": compose_with_newlines_and_a_gap,
  "heading2": compose_with_newlines_and_a_gap,
  "shloka": compose_with_newlines
}
