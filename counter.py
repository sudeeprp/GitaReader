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


def chapter_wordcounts_to_heatmap(chapter_wordcounts):
    chapter_cols = chapter_wordcounts.columns
    chapter_wordcounts['Total'] = chapter_wordcounts.sum(axis=1)
    for chapter in chapter_cols:
        chapter_wordcounts[chapter] /= chapter_wordcounts['Total']
        chapter_wordcounts[chapter] *= 100
    chapter_wordcounts.sort_values(by='Total', ascending=False, inplace=True)
    return chapter_wordcounts
