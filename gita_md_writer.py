import json
from contents2md import shlokaline_to_md, expln_to_meanings, backquote_anchor

def mdcumulate(para_sequence):
  chapters = {}
  def cumulate(chaptitle, para_md):
    if chaptitle not in chapters:
      chapters[chaptitle] = ''
    chapters[chaptitle] += para_md + '\n'

  para_groups = groupadja(para_sequence)
  for group in para_groups:
    cumulate(group_title(group), mdtext(group))
  return chapters

def groupadja(para_sequence):
  para_groups = [{"style": para_sequence[0]["style"], "paras": [para_sequence[0]]}]
  for next, para in zip(para_sequence[1:], para_sequence):
    if next["style"] == para["style"]:
      para_groups[-1]["paras"].append(next)
    else:
      para_groups.append({"style": next["style"], "paras": [next]})
  return para_groups

def group_title(group):
  first_para = group['paras'][0]
  shloka_head = first_para['shloka']
  if shloka_head:
    return shloka_head
  else:
    return first_para['chapter']

def mdtext(group):
  group = merge_contents_in_shloka(group)
  md_texts = [content_to_md(para['content'], group['style'])
    for para in group["paras"]]
  return compose_mds(md_texts, group['style'])

def merge_contents_in_shloka(group):
  if group['style'] == 'shloka':
    merged_para = group['paras'][0]
    for para in group['paras'][1:]:
      merged_para['content'].extend(para['content'])
    group['paras'] = [merged_para]
  return group

def content_to_md(content, style):
  text = content_to_text(content)
  if not text:
    return ''
  try:
    convert_to_md = style2mdtext[style]
    return convert_to_md(text)\
      .replace('.ltstrt', '[').replace('.ltend', ']')\
      .replace('.lnstrt', '(').replace('.lnend', ')')
  except KeyError:
    return ''
  except:
    print(f'error while processing {content}')
    raise

type2text = {
  "text": lambda t: t['content'],
  "anchor": lambda t: f"<a name='{t['name']}'>{t['content']}</a>",
  "extref": lambda t: f"{expln_to_meanings(t['content'])}",
  "phrase": lambda t: f".ltstrt{t['content']}.ltend.lnstrt{t['destination']}.lnend"
}

def content_to_text(content):
  combined_text = ''
  for t in content:
    typename = t['type']
    if typename in type2text:
      combined_text += type2text[typename](t) + '\n'
    else:
      print(f'Warning: ignored type {typename}')
  return combined_text

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
  "explnofshloka": expln_to_meanings,
  "applnotes": backquote_anchor('applnote'),
  "applnotesopener": backquote_anchor('applopener')
}

stylecomposer = {
  ".default": compose_with_newlines_and_a_gap,
  "heading1": compose_with_newlines_and_a_gap,
  "heading2": compose_with_newlines_and_a_gap,
  "shloka": compose_with_newlines,
  "explnofshloka": compose_with_newlines_and_a_gap,
}

def write_chapters(chapters):
  toc = '# Table of Contents\n\n'
  for chaptitle in chapters.keys():
    if chaptitle:
      with open(f'mds/{chaptitle}.md', 'w', encoding='utf8') as chapfile:
        chapfile.write(chapters[chaptitle])
        toc += f'[{chaptitle}]({chaptitle}.md)\n\n'
        print(f'wrote {chaptitle}.md')
  with open('mds/toc.md', 'w', encoding='utf8') as tocfile:
    tocfile.write(toc)

if __name__ == '__main__':
  with open('paras.json', 'r') as para_seq_file:
    print('parsing...')
    para_seq = json.load(para_seq_file)["paragraphs"]
    print(f'got {len(para_seq)} paras. cumulating chapters...')
    chapters = mdcumulate(para_seq)
    print('writing...')
    write_chapters(chapters)
    print('done.')
