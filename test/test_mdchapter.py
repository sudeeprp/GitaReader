import unittest
from gita_md_writer import mdcumulate, groupadja

class MDChapterTest(unittest.TestCase):
  def test_adjacent_paras_of_same_style_are_grouped(self):
    adjacent_paras = [
      {"para": "para1.1", "style": "style1"},
      {"para": "para1.2", "style": "style1"},
      {"para": "para2", "style": "style2"}
    ]
    grouped_paras = groupadja(adjacent_paras)
    self.assertEqual(len(grouped_paras), 2)
    self.assertEqual(grouped_paras[0]["style"], "style1")
    self.assertEqual(len(grouped_paras[0]["paras"]), 2)
    self.assertEqual(grouped_paras[0]["paras"][0]["para"], "para1.1")
    self.assertEqual(grouped_paras[0]["paras"][1]["para"], "para1.2")
    self.assertEqual(len(grouped_paras[1]["paras"]), 1)
    self.assertEqual(grouped_paras[1]["paras"][0]["para"], "para2")

  def test_sample_chapter_written_as_markdown(self):
    gulpables = mdcumulate(sample_chapter_paras)
    first_title = list(gulpables.keys())[0]
    firstchapmd = gulpables[first_title]
    self.assertEqual(first_title, "Chapter 2")
    second_title = list(gulpables.keys())[1]
    shlokamd = gulpables[second_title]
    self.assertEqual(second_title, "2-1 to 2-3")
    with open(f'{first_title}.test.md', 'w', encoding='utf8') as mdfile:
      mdfile.write(firstchapmd)
    with open(f'{second_title}.test.md', 'w', encoding='utf8') as mdfile:
      mdfile.write(shlokamd)
    print(f'see aesthetics: {first_title}.test.md and {second_title}.test.md')

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
  }, {
    "chapter": "Chapter 2", "shloka": "2-1 to 2-3",
    "content": [{
      "type": "text",
      "content": "[ththA] Then, [madhusUdhana:] Krishna [idam vAkyam uvAcha] said this sentence [tam] to Arjuna, [kr`payAviShTam] who was overcome with pity, [ashrupUrNAkulEkShaNam] whose eyes were full of tears: "
    }], "style": "explnofshloka"
  }
]

if __name__ == '__main__':
  unittest.main()
