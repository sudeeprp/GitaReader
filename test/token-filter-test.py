import unittest
import token_filters as filt


class TokenFilterCases(unittest.TestCase):
    def test_punctuations_are_removed(self):
        tokens = filt.remove_punctuation_tokens\
                    (filt.tokenize('Sample, sentence.'))
        second_token = tokens[1]
        self.assertEqual(second_token, 'sentence')
        self.assertEqual(len(tokens), 2)

    def test_stopwords_are_removed(self):
        tokens = filt.significant_words(
                              'Here this is a sample Self. He is [shrImAn], there are no others as well!')
        forbiddens = ['!', 'Here', 'here', 'is', 'a', 'there', 'are', 'as', 'well']
        found_forbiddens = [s for s in forbiddens if s in tokens]
        self.assertTrue(len(found_forbiddens) == 0,
                        f'Found forbidden stopwords: {found_forbiddens}')
        retains = ['He', 'Self']
        retained = [w for w in retains if w in tokens]
        self.assertEqual(len(retained), len(retains))

    def test_catch_phrases_converts_known_word_sequences(self):
        sample_phrases_for_karmayoga = [
            ('He works without attachment, sometimes', "He karmayOga_a_defn, sometimes"),
            ('Working without attachments is great', "karmayOga_a_defn is great"),
            ('work without attachment to outcomes', "karmayOga_a_defn"),
            ('work without attachments towards outcome', "karmayOga_a_defn"),
            ('working without being driven', "karmayOga_a_defn"),
            ('Works without being driven by desire', "karmayOga_a_defn"),
            ('I work without being driven by desires', "I karmayOga_a_defn")
        ]
        for phrase in sample_phrases_for_karmayoga:
            self.assertEqual(filt.catch_phrases(phrase[0]), phrase[1])

    def test_tokenize_splits_punctuations(self):
        sample_phrases_with_punctuation = [
            ("This is what-", ["This", "is", "what", "-"]),
            ("'By the power", ["'", "By", "the", "power"])
        ]
        for phrase in sample_phrases_with_punctuation:
            tokens = filt.tokenize(phrase[0])
            for expected_token in phrase[1]:
                self.assertTrue(expected_token in tokens)


if __name__ == '__main__':
    unittest.main()
