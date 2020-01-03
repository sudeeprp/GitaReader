Feature: Decode the Gita Encoding

  Scenario: Get text for word-counting
    Given a content list
    When the counter asks the decoder for text with phrases
    Then the decoder returns a string with words and phrases

  Scenario: Get text for context-sensitive embedding
    Given a content list
    When the counter asks the decoder for text with content
    Then the decoder returns a string with words
