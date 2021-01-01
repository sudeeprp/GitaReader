import unittest
from gita_md_writer import mdtext

class MDTextTest(unittest.TestCase):
  def test_normal_is_unchanged(self):
    md = mdtext({ "content": [{
        "type": "text", "content": "Just some text"
      }], "style": "normal" })
    self.assertEqual(md, "Just some text")
  
  def test_shloka_is_in_devanagari(self):
    md = mdtext({ "content": [{
        "type": "text", "content": "nArAyaNAya"
      }], "style": "shloka" })
    self.assertEqual(md, "नारायणाय")
    with open('mdsite/omnamo.md', 'w', encoding='utf8') as om:
        om.write(f'''
```shkola
ॐ नमो {md}
```
''')
    print('see omnamo.md in mdsite and listen to it on github & sheets')

  def test_heading1_is_first_level(self):
    md = mdtext({ "content": [{
        "type": "text", "content": "Chapter 2"
      }], "style": "heading1" })
    self.assertEqual(md, "# Chapter 2")

  def test_heading2_is_second_level(self):
    md = mdtext({ "content": [{
          "type": "text", "content": "2-1 to 2-3"
      }], "style": "heading2" })
    self.assertEqual(md, '## 2-1 to 2-3')
      
  def test_only_text_content_in_md(self):
    md = mdtext({ "content": [{
        "type": "anchor", "content": "donotinclude"
      }, {
        "type": "text", "content": "Chapter 2"
      }], "style": "heading1"})
    self.assertNotIn('donotinclude', md)
    self.assertIn('Chapter 2', md)

if __name__ == '__main__':
  unittest.main()
