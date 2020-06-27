Feature: explore

  Scenario: write context-specific word embeddings
    Given the text
      """
      Attachments do tie us down. We desired the universe.
      Few of us desire the Lord. The Self desires the Lord.
      """
    And text preparation without sanskrit, shloka
    And delimitation with separators inserted
    And word-wise BERT tokenization
    And word-wise reduction by summing last 4
    When the explorer asks for embeddings
    Then word-wise embeddings are stored in BERT-sepinsert-4sum.csv
