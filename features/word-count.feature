Feature: Word count

  Scenario Outline: Count of single non-stop words
    Given the sentence <sentence>
    When the reader asks for word count
    Then <counts> should be reported

    Examples:
      | sentence                                         | counts                                                                         |
      | The [puruSha sUkta] says:                        | [('puruSha', 1), ('sUkta', 1), ('says', 1)]                                    |
      | 'By knowing Him alone, a person attains moksha.' | [('knowing', 1), ('Him', 1), ('alone', 1), ('person', 1), ('attains', 1), ('moksha', 1)] |

  Scenario: Word count in a paragraph
    Given a paragraph of text
    """
    As described before, the entire universe belongs to Me, consisting of conscious and
    non-conscious elements. The universe periodically comes into being from Me.
    At the time of its destruction, it comes back to rest in Me. It is sustained in Me alone.
    It is situated as though it were My body, having Me as its owner.
    """
    When the reader asks for word count
    Then some counts are reported

  Scenario: Bigram count in a paragraph
    Given a paragraph of text
    """
    As described before, the entire universe belongs to Me, consisting of conscious and
    non-conscious elements. The universe periodically comes into being from Me.
    At the time of its destruction, it comes back to rest in Me. It is sustained in Me alone.
    It is situated as though it were My body, having Me as its owner.
    """
    When the reader asks for bigram count
    Then some counts are reported
