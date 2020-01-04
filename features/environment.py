

def before_feature(context, scenario):
    if scenario.name == 'Context sensitive embeddings':
        from pytorch_pretrained_bert import BertTokenizer, BertModel
        print('Preparing BERT...', end='')
        context.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        context.model = BertModel.from_pretrained('bert-base-uncased')
        print('done')
