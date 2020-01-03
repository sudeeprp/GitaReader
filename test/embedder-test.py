import unittest
import embedder


class DelimiterTest(unittest.TestCase):
    def test_normal_is_delimited(self):
        normal_para = {
              "id": "*", "chapter": "Chapter 2", "shloka": "2-16",
              "content": [{
                  "type": "extref",
                  "destination": "[vishNu purANa], 2-12-43:",
                  "content": "[vishNu purANa], 2-12-43:"
                }, {
                  "type": "text",
                  "content": " Sri Parashara has said- \u2018The Self is the embodiment of knowledge.\u2019"
                }],
              "style": "normal"
            }
        text = embedder.para_to_delimited_text(normal_para)
        self.assertTrue("[vishNu purANa], 2-12-43:" in text)
        self.assertTrue("Parashara" in text)

    def test_shloka_is_not_delimited(self):
        shloka_para = {
              "id": "*", "chapter": "Chapter 1", "shloka": "1-1 to 1-11",
              "content": [{
                  "type": "text",
                  "content": "dhr'tarAShTra uvAcha"
              }],
              "style": "shloka"
            }
        self.assertEqual('', embedder.para_to_delimited_text(shloka_para))

    def test_expln_is_delimited_without_sanskrit(self):
        expln_para = {
              "id": "*", "chapter": "Chapter 1", "shloka": "1-1 to 1-11",
              "content": [{
                  "type": "text",
                  "content": "[dhr'tarAShTra uvAcha] Dhrtarashtra said - [sanjaya] Sanjaya, [mAmakA:] my people"
              }],
              "style": "explnofshloka"
            }
        self.assertEqual('[CLS]  Dhrtarashtra said -  Sanjaya,  my people. [SEP]',
                         embedder.para_to_delimited_text(expln_para))


if __name__ == '__main__':
    unittest.main()
