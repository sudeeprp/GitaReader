import re
import torch
import decoder


# Max distance of similar words = 0.3734787106513977
# Minimum distance of dissimilar tokens = 0.5230562686920166 (the)
def add_cls_and_insert_sep(para_text):
    para_text = '[CLS] ' + para_text
    para_text = para_text.replace('. ', '. [SEP] ')
    if para_text[-1] != '.':
        para_text += '.'
    para_text += ' [SEP]'
    return para_text


# Max distance of similar words = 0.41177988052368164
# Minimum distance of dissimilar tokens = 0.5039441585540771 (the)
def add_cls_and_sep(para_text):
    return '[CLS] ' + para_text + ' [SEP]'


def para_to_delimited_text(para):
    if para["style"].lower() == 'shloka':
        return ''
    para_text = decoder.text_content(para["content"])
    if para["style"] == 'explnofshloka':
        para_text = re.sub(r'\[[^]]+\]', '', para_text)
    return add_cls_and_insert_sep(para_text)
    # return add_cls_and_sep(para_text)


def pool_per_word(tokenlist, token_embeddings):
    token_embedding_pairs = []
    for i, token in enumerate(tokenlist):
        t_embedding = token_embeddings[i]
        # t_last4 = torch.cat((t_embedding[-1], t_embedding[-2],
        #                      t_embedding[-3], t_embedding[-4]), dim=0)
        t_last4 = torch.sum(t_embedding[-4:], dim=0)
        token_embedding_pairs.append((token, t_last4))
    return token_embedding_pairs


def para_to_word_embeddings(tokenizer, model, para):
    text = para_to_delimited_text(para)
    # tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    tokens = tokenizer.tokenize(text)
    token_tensor = torch.tensor(tokenizer.convert_tokens_to_ids(tokens))
    # can use different segments for different sentences
    # segment_tensor = torch.tensor([1] * len(tokens))
    # model = BertModel.from_pretrained('bert-base-uncased')
    model.eval()
    with torch.no_grad():
        encoded_layers, _ = model(token_tensor.unsqueeze(0))
    # print_sample(encoded_layers)
    token_embeddings = torch.stack(encoded_layers, dim=0)
    token_embeddings = torch.squeeze(token_embeddings, dim=1)
    token_embeddings = token_embeddings.permute(1, 0, 2)
    # print(f'-> token_embeddings size: {token_embeddings.size()}')
    return pool_per_word(tokens, token_embeddings)


def print_sample(encoded_layers):
    print(f'Layers: {len(encoded_layers)}')
    print(f'Batches/Sentences: {len(encoded_layers[0])}')
    print(f'Tokens in 1st sentence: {len(encoded_layers[0][0])}')
    print(f'Hidden units: {len(encoded_layers[0][0][0])}')
