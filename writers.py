import decoder
import counter
import in_para_allcontent


def write_overall_word_counts(paras):
    text = ''
    for para in paras:
        if para["style"].lower() != 'shloka':
            text += decoder.text_with_phrases(in_para_allcontent.contentlist(para)) + ' '
    word_counts = counter.count_significant_words(text)
    counter.write_as_csv('GitaBhashya-try-counts.csv', word_counts)
    print("Wrote counts to GitaBhashya-try-counts.csv")


def write_chapter_wordmap(paras):
    pass
