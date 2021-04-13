import translit
import re

def shlokaline_to_md(shlokaline):
  bare_shloka = no_sq_encl(shlokaline)
  if not bare_shloka:
    return ''
    
  return f'''```shloka-sa
{translit.gita_to_devanagari(bare_shloka)}
```
```shloka-sa-hk
{translit.to_harward_kyoto(bare_shloka)}
```'''

def expln_to_meanings(explnline):
  explnseq = [x.strip() for x in re.split('(\[[^\]]*\])', explnline) if x]
  meaningitems = []
  for phrase in explnseq:
    if phrase.startswith('['):
      devanagari = translit.gita_to_devanagari(no_sq_encl(phrase))
      meaningitems.append(f'`{devanagari}` `{translit.to_harward_kyoto(phrase)}`')
    else:
      meaningitems.append(phrase.strip())
  return ' '.join(meaningitems)

def no_sq_encl(para_text):
  return para_text.strip().replace('[', '').replace(']', '')
