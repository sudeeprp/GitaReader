import unittest
from gita_md_writer import mdcumulate

class MDChapterTest(unittest.TestCase):
  def test_sample_chapter_written_as_markdown(self):
    chapters = mdcumulate(sample_chapter_paras)
    first_title = list(chapters.keys())[0]
    firstchapmd = chapters[first_title]
    with open(f'{first_title}.test.md', 'w', encoding='utf8') as mdfile:
      mdfile.write(firstchapmd)
    print(f'check aesthetics of {first_title}.test.md')

sample_chapter_paras = [{
    "chapter": "Chapter 2", "shloka": "",
    "content": [{
      "type": "anchor", "name": "_Chapter_2", "content": ""
    }, {
      "type": "text", "content": "Chapter 2"
    }], "style": "heading1"
  }, {
    "chapter": "Chapter 2", "shloka": "2-1 to 2-3",
    "content": [{
      "type": "text", "content": "2-1 to 2-3"
    }], "style": "heading2"
  }, {
    "chapter": "Chapter 2", "shloka": "2-1 to 2-3",
    "content": [{
      "type": "text",
      "content": "tam tathA kr`payAviShTam ashrupUrNAkulEkShaNam |"
    }], "style": "shloka"
  }
]

if __name__ == '__main__':
  unittest.main()
