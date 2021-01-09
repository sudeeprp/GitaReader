import unittest
from gita_md_writer import mdcumulate

class MDShlokaTest(unittest.TestCase):
  def test_shloka_lines_are_merged_in_multiline(self):
    chapters = mdcumulate(sample_shloka_sequence)
    first_title = list(chapters.keys())[0]
    mdcontent = chapters[first_title]
    print(f'mdcontent {mdcontent}')
    self.assertTrue(mdcontent.startswith('```'))
    self.assertTrue(mdcontent.endswith('```'))

sample_shloka_sequence = [    {
    "chapter": "Chapter 1", "shloka": "1-1",
    "content": [
      {"type": "text", "content": "prathama |"}
    ], "style": "shloka"
  }, {
    "chapter": "Chapter 1", "shloka": "1-1",
    "content": [
      {"type": "text", "content": "dvitIya ||"}
    ], "style": "shloka"
  },
]

if __name__ == '__main__':
  unittest.main()
