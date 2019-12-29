import in_para_allcontent
import gita_encode
import decoder
import counter


docx_as_dict = gita_encode.encode_doc('GitaBhashya-try.docx')
paras = in_para_allcontent.paralist(docx_as_dict)

text = ''
for para in paras:
    if para["style"].lower() != 'shloka':
        text += decoder.text_with_phrases(in_para_allcontent.contentlist(para)) + ' '

word_counts = counter.count_significant_words(text)
counter.write_as_csv('GitaBhashya-try.csv', word_counts)
