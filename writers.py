import pandas as pd
import decoder
import counter
import in_para_allcontent


def paras_without_shlokas(paras):
    return [para for para in paras if para["style"].lower() != 'shloka']


def write_wordcounts_as_csv(filename, word_count_pairs):
    word_count_pairs.sort(key=lambda x: x[1], reverse=True)
    with open(filename, 'w', encoding='utf-8') as output_file:
        for word_count_pair in word_count_pairs:
            output_file.write(str(word_count_pair[0]) + ',' + str(word_count_pair[1]) + '\n')


def write_overall_word_counts(paras):
    text = ''
    for para in paras_without_shlokas(paras):
        text += decoder.text_with_phrases(in_para_allcontent.contentlist(para)) + ' '
    word_counts = counter.count_significant_words(text)
    write_wordcounts_as_csv('GitaBhashya-try-counts.csv', word_counts)
    print("Wrote counts to GitaBhashya-try-counts.csv")


def append(chapter_texts, chapter_name, text):
    if chapter_name not in chapter_texts:
        chapter_texts[chapter_name] = ''
    chapter_texts[chapter_name] += text


def write_chapter_wordmap(paras):
    chapter_texts = {}
    for para in paras_without_shlokas(paras):
        append(chapter_texts, para['chapter'],
               decoder.text_with_phrases(in_para_allcontent.contentlist(para)) + ' ')
    chapter_word_counts = pd.DataFrame()
    for chapter in chapter_texts:
        word_counts = counter.count_significant_words(chapter_texts[chapter])
        for count_pair in word_counts:
            chapter_word_counts.at[count_pair[0], chapter] = count_pair[1]
    counter.chapter_wordcounts_to_heatmap(chapter_word_counts)
    chapter_word_counts.to_csv('GitaBhashya-try-chapmap.csv')
    print("Wrote chapter-wise counts to GitaBhashya-try-chapmap.csv")
