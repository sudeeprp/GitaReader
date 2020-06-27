import unittest
import verse_writer


class VerseMakerTests(unittest.TestCase):
    def test_shlokas_are_formed_in_two_lines(self):
        first_line = 'first line|'
        second_line = 'second line||'
        paras = [{
          "shloka": "2-18",
          "content": [{"content": "["}],
          "style": "shloka"
        }, {
          "shloka": "2-18",
          "content": [{"content": first_line}],
          "style": "shloka"
        }, {
          "shloka": "2-18",
          "content": [{"content": second_line}],
          "style": "shloka"
        }]
        content = verse_writer.blank_content()
        for i in range(len(paras)):
            content = verse_writer.form_presentable(paras, i, content)
        self.assertTrue(first_line in content['shloka'])
        self.assertTrue(second_line in content['shloka'])

    def test_translation_is_filled(self):
        paras = [{
          "shloka": "2-18",
          "content": [{"content": "this is a translation"}],
          "style": "explnofshloka"
        }]
        content = verse_writer.form_presentable(paras, 0, verse_writer.blank_content())
        self.assertGreater(len(content['translation']), 1)

    def test_2d_insights_is_filled(self):
        paras = [{
          "shloka": "2-18",
          "content": [{"content": "content before insight"}],
          "style": "normal"
        }, {
          "shloka": "2-18",
          "content": [{"content": "the insight"}],
          "style": "applnotes"
        }, {
            "shloka": "2-18",
            "content": [{"content": "content after the insight"}],
            "style": "normal"
        }]
        content = verse_writer.blank_content()
        for i in range(len(paras)):
            content = verse_writer.form_presentable(paras, i, content)
        self.assertEqual(2, len(content['insights']))

    def test_commentary_filler_fills_blank_insight(self):
        content = verse_writer.blank_content()
        element = {"content": "new stuff"}
        content = verse_writer.commentary_filler(element, content)
        self.assertTrue(content["insights"][-1][1].startswith("new stuff"))

    def test_commentary_filler_appends_existing_sentence_with_break(self):
        content = {"insights": [["", "old stuff."]]}
        element = {"content": "new stuff"}
        content = verse_writer.commentary_filler(element, content)
        self.assertTrue(content["insights"][-1][1].startswith("old stuff.<br>new stuff"))

    def test_commentary_filler_continues_incomplete_sentence_without_break(self):
        content = {"insights": [["", "old stuff"]]}
        element = {"content": "new stuff"}
        content = verse_writer.commentary_filler(element, content)
        self.assertTrue(content["insights"][-1][1].startswith("old stuffnew stuff"))

    def test_successive_commentary_paras_from_same_shloka_are_merged(self):
        paras = [{
          "shloka": "1-26 to 1-47",
          "content": [{"content": "Sanjaya said - "}],
          "style": "normal"
        }, {
          "shloka": "1-26 to 1-47",
          "content": [{"content": "Arjuna is a person with a great mind."}],
          "style": "normal"
        }]
        content = verse_writer.blank_content()
        for i in range(len(paras)):
            content = verse_writer.form_presentable(paras, i, content)
        self.assertEqual(1, len(content['insights']))

    def test_content_boundary_is_recognized_at_the_end(self):
        paras = [{
            "shloka": "2-18"
        }]
        self.assertTrue(verse_writer.content_boundary(paras, 0))

    def test_content_boundary_is_recognized_when_shloka_changes(self):
        paras = [{"shloka": "2-18"}, {"shloka": "2-18"}, {"shloka": "2-19"}, {"shloka": "2-19"}]
        self.assertTrue(verse_writer.content_boundary(paras, 1))

    def test_content_boundary_is_not_recognized_in_same_shloka(self):
        paras = [{
            "shloka": "2-18"
        }, {
            "shloka": "2-18"
        }]
        self.assertFalse(verse_writer.content_boundary(paras, 0))


if __name__ == '__main__':
    unittest.main()
