from behave import given, when, then
import decoder


@given('a content list')
def step_impl(context):
    context.decode_pack = {
        'decoder_input': [
            {"type": "text", "content": "Our skill lies in "},
            {"type": "phrase", "destination": "karmayOga_a_defn",
             "content": "working without attachment"},
            {"type": "text", "content": " and it's a beautiful thing."}
        ]
    }


@when('the counter asks the decoder for text with phrases')
def step_impl(context):
    context.decode_pack['decoder_output'] = \
        decoder.text_with_phrases(context.decode_pack['decoder_input'])


@then('the decoder returns a string with words and phrases')
def step_impl(context):
    decoder_output = context.decode_pack['decoder_output']
    assert decoder_output == "Our skill lies in karmayOga_a_defn and it's a beautiful thing.",\
                             f"decoder output is >{decoder_output}<"
