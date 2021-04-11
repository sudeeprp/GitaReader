import unittest
from gita_md_writer import mdcumulate

class MDShlokaTest(unittest.TestCase):
  def test_shloka_lines_are_merged_in_multiline(self):
    chapters = mdcumulate(two_line_shloka)
    first_title = list(chapters.keys())[0]
    mdlines = chapters[first_title].split('\n')
    _, end = self.check_section(mdlines, '```shloka-sa', '```')
    _, end = self.check_section(mdlines, '```shloka-sa-hk', '```', end + 1)
    _, end = self.check_section(mdlines, '```shloka-sa', '```', end + 1)
    _, end = self.check_section(mdlines, '```shloka-sa-hk', '```', end + 1)

  def check_section(self, lines, startline, endline, startindex = 0):
    start = lines.index(startline, startindex)
    end = lines.index(endline, startindex)
    self.assertTrue(start < end)
    return start, end

two_line_shloka = [{
  "chapter": "Chapter 1", "shloka": "1-1",
  "content": [
    {"type": "text", "content": "prathama |"}
  ], "style": "shloka"
}, {
  "chapter": "Chapter 1", "shloka": "1-1",
  "content": [
    {"type": "text", "content": "dvitIya ||"}
  ], "style": "shloka"
}]

if __name__ == '__main__':
  unittest.main()
