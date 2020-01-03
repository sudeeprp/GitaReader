Feature: Context sensitive embeddings

  Scenario: Make embeddings for words in a sentence
    Given a paragraph with one sentence of plain text
    When the reader asks for embeddings
    Then each word must have an embedding

  Scenario: Make embeddings for words in multiple sentences
    Given a paragraph with three sentence of plain text
    When the reader asks for embeddings
    Then each word must have an embedding
