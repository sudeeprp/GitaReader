import json
import gita_encode
import in_para_allcontent
import writers

docx_as_dict = gita_encode.encode_doc('GitaBhashya-try.docx')
with open('GitaBhashya-try-encoding.json', 'w') as encoded_file:
    json.dump(docx_as_dict, encoded_file, indent=2)
    print("Wrote the encoding to GitaBhashya-try-encoding.json")

paras = in_para_allcontent.paralist(docx_as_dict)
writers.write_overall_word_counts(paras)
writers.write_chapter_wordmap(paras)
