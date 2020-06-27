import math
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


def distrpercent_to_heatmap_cells(chaper_percent_pairs):
    html_cells = ''
    for chapter_percent in chaper_percent_pairs:
        chapter = f'{int(chapter_percent[0]):02d}'
        percent = chapter_percent[1]
        heat = percent / 100
        if math.isnan(heat):
            heat = 0
        if heat > 0.05:
            rescale_base = 0.2
            heat = heat * (1 - rescale_base) + rescale_base
        hsla_green = '90,100%,50%'
        hsla_pastelgreen = '120,60%,70%'
        html_cells += f'<td style="background-color: hsla({hsla_pastelgreen},{heat:.2f});">' \
                      f'{chapter}</td>'
    return html_cells


def make_html_heatmap(chapter_word_counts, filename):
    chapterHeadings = [h for h in chapter_word_counts.columns.values.tolist()
                       if isinstance(h, str) and h.startswith('Chapter')]
    html_rows = ''
    for row in range(1000):
        percent_distr_per_chapter = chapter_word_counts.iloc[row]
        current_word = percent_distr_per_chapter.name
        chapter_percent_pair = [(chapter.split()[-1], percent_distr_per_chapter[chapter])
                                for chapter in chapterHeadings]
        html_rows += \
            f'<tr><td>{current_word}</td>' \
            f'{distrpercent_to_heatmap_cells(chapter_percent_pair)}</tr>\n'
    with open(filename, 'w') as htmlfile:
        htmlfile.write(f'<table style="font-variant-numeric: tabular-nums;">\n'
                       f'{html_rows}'
                       f'</table>\n')


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
    make_html_heatmap(chapter_word_counts, 'GitaBhashya-try-heatmap.html')
