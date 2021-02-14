import translit
import re

def shlokaline_to_md(shlokaline):
  return f'''```shloka-sa
{translit.gita_to_devanagari(shlokaline)}
```
```shloka-sa-hk
{translit.to_harward_kyoto(shlokaline)}
```'''

def expln_to_meanings(explnline):
  explnseq = [x.strip() for x in re.split('(\[[^\]]*\])', explnline) if x]
  meaningitems = []
  for phrase in explnseq:
    if phrase.startswith('['):
      devanagari = translit.gita_to_devanagari(
        phrase.strip().replace('[', '').replace(']', ''))
      meaningitems.append(f'`{devanagari}` `{phrase}`')
    else:
      meaningitems.append(phrase.strip())
  return ' '.join(meaningitems)
