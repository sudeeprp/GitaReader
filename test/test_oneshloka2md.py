import unittest
from gita_md_writer import mdcumulate

class MDShlokaTest(unittest.TestCase):
  def test_shloka_lines_are_merged_in_multiline(self):
    gulpables = mdcumulate(two_line_shloka)
    first_title = list(gulpables.keys())[0]
    mdlines = gulpables[first_title].split('\n')
    content, end = self.get_section(mdlines, '```shloka-sa', '```')
    self.assertIn('प्रथम', content)
    self.assertIn('द्वितीय', content)
    content, end = self.get_section(mdlines, '```shloka-sa-hk', '```', end + 1)
    self.assertIn('prathama', content)
    self.assertIn('dvitIya', content)

  def get_section(self, lines, startline, endline, startindex = 0):
    start = lines.index(startline, startindex)
    end = lines.index(endline, startindex)
    self.assertTrue(start < end)
    content = '\n'.join(lines[start+1:end])
    return content, end

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
