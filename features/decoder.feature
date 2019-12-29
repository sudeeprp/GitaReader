Feature: Decode the Gita Encoding

  Scenario: Get text for word-counting
    Given a content list
    When the counter asks the decoder for text with phrases
    Then the decoder returns a string with words and phrases
