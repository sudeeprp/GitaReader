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
                              'Here this is a sample. [shrImAn], there are others as well!')
        forbiddens = ['!', 'Here', 'here', 'is', 'a', 'there', 'are', 'as', 'well']
        found_forbiddens = [s for s in forbiddens if s in tokens]
        self.assertTrue(len(found_forbiddens) == 0,
                        f'Found forbidden stopwords: {found_forbiddens}')

    def test_tokenize_lowers_case_of_first_char(self):
        tokens = filt.tokenize("I have done it. But he said 'I have done it' too. 'Who did it?'")
        forbiddens = ['I', 'But', 'Who']
        found_forbiddens = [s for s in forbiddens if s in tokens]
        self.assertTrue(len(found_forbiddens) == 0,
                        f'Found leftover uppercase-starts: {found_forbiddens}')
        self.assertTrue('i' in tokens)
        self.assertTrue('but' in tokens)
        self.assertTrue('who' in tokens)


if __name__ == '__main__':
    unittest.main()
