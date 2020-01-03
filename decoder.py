

def text_with_phrases(contentlist):
    text = ''
    for content in contentlist:
        if content["type"] == 'phrase':
            text += content["destination"]
        else:
            text += content["content"]
    return text


def text_content(contentlist):
    text = ''
    for content in contentlist:
        text += content["content"]
    return text
