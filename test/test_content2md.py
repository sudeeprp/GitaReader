import unittest
from gita_md_writer import content_to_md

class MDTextTest(unittest.TestCase):
  def test_normal_is_unchanged(self):
    md = content_to_md([{"type": "text", "content": "Just some text"}],
      "normal")
    self.assertEqual(md, "Just some text")
  
  def test_devanagari_goes_in_md(self):
    md = content_to_md([{"type": "text", "content": "nArAyaNAya"}],
      "shloka")
    self.assertIn("नारायणाय", md)

  def test_heading1_is_first_level(self):
    md = content_to_md([{"type": "text", "content": "Chapter 2"}],
      "heading1")
    self.assertEqual(md, "# Chapter 2")

  def test_heading2_is_second_level(self):
    md = content_to_md([{"type": "text", "content": "2-1 to 2-3"}],
      "heading2")
    self.assertEqual(md, '## 2-1 to 2-3')
      
  def test_only_text_content_in_md(self):
    md = content_to_md([
      {"type": "not-text", "content": "donotinclude"},
      {"type": "text", "content": "Chapter 2"}],
      "heading1")
    self.assertNotIn('donotinclude', md)
    self.assertIn('Chapter 2', md)

  def test_doesnt_crash_on_unknown_style(self):
    content_to_md([{"type": "text", "content": "any"}], 'unknown-style')

  def test_explnofshloka_puts_translations(self):
    md = content_to_md([
      {"type": "text", "content": "[aham] I [asmi] am"}],
      "explnofshloka")
    self.assertEqual(md, '`अहम्` `[aham]` I `अस्मि` `[asmi]` am')

  def test_translit_is_in_kh(self):
    md = content_to_md([
      {"type": "text", "content": "[kr`payAviShTam] who was overcome with pity"}
    ], "explnofshloka")
    self.assertEqual(md, '`कृपयाविष्टम्` `[kRpayAviSTam]` who was overcome with pity')

if __name__ == '__main__':
  unittest.main()
