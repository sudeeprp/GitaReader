import unittest
import translit


class TransliterationCase(unittest.TestCase):
    def test_Gita_is_converted_to_devanagari(self):
        expected_mapping = {
            "siddhayE": "सिद्धये",
            "sanga": "सङ्ग",
            "shankha": "शङ्ख",
            "karmaNa:": "कर्मणः",
            "kr`ShNa": "कृष्ण",
            "vartana": "वर्तन",
            "sanga karmaNa: vartana": "सङ्ग कर्मणः वर्तन",
            "ichChA": "इच्छा",
            "prakr'tisthO": "प्रकृतिस्थो",
            "bhunktE": "भुङ्क्ते",
            "saMjnai": "संज्ञै",
            "sO_mr`tatvAya": "सोऽमृतत्वाय",
            "yajna": "यज्ञ",
            "swadharmE": "स्वधर्मे"
        }
        for transliterated in expected_mapping:
            self.assertEqual(expected_mapping[transliterated],
                             translit.gita_to_devanagari(transliterated))


if __name__ == '__main__':
    unittest.main()
