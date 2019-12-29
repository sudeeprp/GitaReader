

def text_with_phrases(contentlist):
    text = ''
    for content in contentlist:
        if content["type"] == 'phrase':
            text += content["destination"]
        else:
            text += content["content"]
    return text
