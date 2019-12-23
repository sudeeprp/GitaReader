from collections import Counter
from nltk import bigrams
from nltk import FreqDist
import token_filters as filters


def count_words(words):
    return Counter(words).most_common()


def count_bigrams(words):
    bigram_counts = []
    word_freq = FreqDist(bigrams(words))
    for bigram, count in word_freq.items():
        printable_bigram = (str(bigram[0]) + " " + str(bigram[1])).replace(',', ' ')
        bigram_counts.append((printable_bigram, count))
    return bigram_counts


def count_significant_words(text):
    return count_words(filters.significant_words(text))


def write_as_csv(filename, word_count_pairs):
    word_count_pairs.sort(key=lambda x: x[1], reverse=True)
    with open(filename, 'w') as output_file:
        for word_count_pair in word_count_pairs:
            output_file.write(str(word_count_pair[0]) + ',' + str(word_count_pair[1]) + '\n')
