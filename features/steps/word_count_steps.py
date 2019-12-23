from behave import given, when, then
import counter
import token_filters as filt


@given("the sentence {sentence}")
def step_impl(context, sentence):
    context.sentence = sentence


@given("a paragraph of text")
def step_impl(context):
    context.sentence = context.text


@when("the reader asks for word count")
def step_impl(context):
    context.word_counts = counter.count_significant_words(context.sentence)


@when("the reader asks for bigram count")
def step_impl(context):
    context.word_counts = counter.count_bigrams(filt.tokenize(context.sentence))

@then("{counts} should be reported")
def step_impl(context, counts):
    assert str(context.word_counts) == counts, f'\nCounts expected: {counts}\nCounts received: {context.word_counts}'


@then("some counts are reported")
def step_impl(context):
    assert len(context.word_counts) > 0
