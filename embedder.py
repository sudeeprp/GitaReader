import re
import torch
from pytorch_pretrained_bert import BertTokenizer, BertModel, BertForMaskedLM
import decoder


def para_to_delimited_text(para):
    if para["style"].lower() == 'shloka':
        return ''
    para_text = decoder.text_content(para["content"])
    if para["style"] == 'explnofshloka':
        para_text = re.sub('\[[^]]+\]', '', para_text)
    para_text = '[CLS] ' + para_text
    para_text = para_text.replace('. ', '. [SEP] ')
    if para_text[-1] != '.':
        para_text += '.'
    para_text += ' [SEP]'
    return para_text


def para_to_word_embeddings(para):
    text = para_to_delimited_text(para)
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    tokens = tokenizer.tokenize(text)
    token_tensor = torch.tensor(tokenizer.convert_tokens_to_ids(tokens))
    # segment_tensor = torch.tensor([1] * len(tokens))
    model = BertModel.from_pretrained('bert-base-uncased')
    # model = BertModel.from_pretrained(r'C:\WorkArea-in\bert-base')
    model.eval()
    with torch.no_grad():
        encoded_layers, _ = model(token_tensor.unsqueeze(0))
    print(f'Layers: {len(encoded_layers)}')
    print(f'Batches/Sentences: {len(encoded_layers[0])}')
    print(f'Tokens in 1st sentence: {len(encoded_layers[0][0])}')
    print(f'Hidden units: {len(encoded_layers[0][0][0])}')
    token_embeddings = torch.stack(encoded_layers, dim=0)
    token_embeddings = torch.squeeze(token_embeddings, dim=1)
    token_embeddings = token_embeddings.permute(1, 0, 2)
    print(f'-> token_embeddings size: {token_embeddings.size()}')
    return token_embeddings
