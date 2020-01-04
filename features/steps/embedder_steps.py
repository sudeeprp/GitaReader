from behave import given, when, then
from scipy.spatial.distance import cosine
import embedder


def make_para_with_text(text):
    return {"id": "*", "chapter": "Chapter 2", "shloka": "2-16",
            "content": [{
                "type": "text",
                "content": text
            }],
            "style": "normal"}


@given("a paragraph with one sentence of plain text")
def step_impl(context):
    context.para = make_para_with_text("The Lord is powerful.")


@given("a paragraph with three sentence of plain text")
def step_impl(context):
    context.para = make_para_with_text("The Lord is powerful. He is adorable. He is compassionate.")


@given("the text")
def step_impl(context):
    context.para = context.para = make_para_with_text(context.text)


@given("we consider tokens starting with {prefix} to be similar")
def step_impl(context, prefix):
    context.token_is_similar = lambda x: x.lower().startswith(prefix)


@when("the reader asks for embeddings")
def step_impl(context):
    context.embedding = embedder.para_to_word_embeddings\
                            (context.tokenizer, context.model, context.para)


@then("each word must have an embedding")
def step_impl(context):
    number_of_embeddings = len(context.embedding)
    assert number_of_embeddings > 0


@then("words we consider similar have cosine distance less than {max_distance:f}")
def step_impl(context, max_distance):
    related_distance_reports = []
    context.first_embedding = None
    for token_embedding in context.embedding:
        token = token_embedding[0]
        embedding = token_embedding[1]
        if context.token_is_similar(token):
            if context.first_embedding is None:
                context.first_embedding = embedding
            else:
                distance = cosine(context.first_embedding, embedding)
                if distance >= max_distance:
                    print(f'Cosine distance of "{token}" not close enough: {distance}')
                related_distance_reports.append(distance)
    print(f'Max distance of similar words = {max(related_distance_reports)}')
    assert max(related_distance_reports) < max_distance


@then("dissimilar tokens have cosine distance more than {max_distance:f}")
def step_impl(context, max_distance):
    unrelated_distances = []
    for token_embedding in context.embedding:
        token = token_embedding[0]
        embedding = token_embedding[1]
        if not context.token_is_similar(token):
            distance = cosine(context.first_embedding, embedding)
            if distance < max_distance:
                print(f'Cosine distance of "{token}" too close: {distance}')
            unrelated_distances.append((token, distance))
    unrelated_distances.sort(key=lambda x: x[1])
    print('Closest unrelated tokens:')
    for i in range(max([10, len(unrelated_distances)])):
        print(f'{unrelated_distances[i][0]}: {unrelated_distances[i][1]}')
    assert unrelated_distances[0][1] >= max_distance
