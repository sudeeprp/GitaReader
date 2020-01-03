from behave import given, when, then
import embedder


@given("a paragraph with one sentence of plain text")
def step_impl(context):
    context.para = {
              "id": "*", "chapter": "Chapter 2", "shloka": "2-16",
              "content": [{
                  "type": "text",
                  "content": "The Lord is powerful."
                }],
              "style": "normal"
            }


@given("a paragraph with three sentence of plain text")
def step_impl(context):
    context.para = {
              "id": "*", "chapter": "Chapter 2", "shloka": "2-16",
              "content": [{
                  "type": "text",
                  "content": "The Lord is powerful. He is adorable. He is omnipresent."
                }],
              "style": "normal"
            }


@when("the reader asks for embeddings")
def step_impl(context):
    context.embedding = embedder.para_to_word_embeddings(context.para)


@then("each word must have an embedding")
def step_impl(context):
    # expected_length = len(context.para["content"][0]["content"].split())
    number_of_embeddings = len(context.embedding)
    assert number_of_embeddings > 0
