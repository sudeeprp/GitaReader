Feature: Context sensitive embeddings

  Scenario: Make embeddings for words in a sentence
    Given a paragraph with one sentence of plain text
    When the reader asks for embeddings
    Then each word must have an embedding

  Scenario: Make embeddings for words in multiple sentences
    Given a paragraph with three sentence of plain text
    When the reader asks for embeddings
    Then each word must have an embedding

  Scenario: Check similarity of grammatically related words
    Given the text
      """
      Attachments do tie us down. We desired the universe.
      Few of us desire the Lord. The Self desires the Lord.
      """
    And we consider tokens starting with desire to be similar
    When the reader asks for embeddings
    Then words we consider similar have cosine distance less than 0.47
    And dissimilar tokens have cosine distance more than 0.5
