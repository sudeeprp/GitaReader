import unittest
import token_filters as filt


class TokenFilterCases(unittest.TestCase):
    def test_punctuations_are_removed(self):
        tokens = filt.remove_punctuations\
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


if __name__ == '__main__':
    unittest.main()
