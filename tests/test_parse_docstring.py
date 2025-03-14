

from ftl_doc_agent._function_type_hints_utils import _parse_google_format_docstring




def test_1():
    main_doc, param_descriptions, return_doc = _parse_google_format_docstring(
                """
        Update the docstring for the function.

        Args:
            docstring: A string containing the docstring for the function.
            function: the name of the function.
        """)
    print(main_doc, param_descriptions, return_doc)

    assert main_doc == "Update the docstring for the function."
    assert param_descriptions == {'docstring': 'A string containing the docstring for the function.', 'function': 'the name of the function.'}
    assert return_doc is None


def test_2():
    """
    This should pass but it currently fails due to not parsing out the type in the argument name.
    See: args_split_re in smolagents/src/smolagents/_function_type_hints_utils.py
    """

    main_doc, param_descriptions, return_doc = _parse_google_format_docstring(
                """
        Update the docstring for the function.

        Args:
            docstring (str): A string containing the docstring for the function.
            function (str): the name of the function.
        """)
    print(main_doc, param_descriptions, return_doc)

    assert main_doc == "Update the docstring for the function."
    assert param_descriptions == {'docstring': 'A string containing the docstring for the function.', 'function': 'the name of the function.'}
    assert return_doc is None

def test_3():


    main_doc, param_descriptions, return_doc = _parse_google_format_docstring(
        """
        Determine if two strings are anagrams of each other.

        An anagram is a rearrangement of the characters of one string to form another,
        using all the original letters exactly once.

        Args:
            s (str): The first input string consisting of lowercase English letters.
            t (str): The second input string consisting of lowercase English letters.

        Returns:
            bool: True if `t` is an anagram of `s`, False otherwise.

        """)

    print(main_doc, param_descriptions, return_doc)

    assert main_doc.startswith("Determine if two strings are anagrams of each other.")
    assert param_descriptions == {'s': 'The first input string consisting of lowercase English letters.', 't': 'The second input string consisting of lowercase English letters.'}
    assert return_doc == "bool: True if `t` is an anagram of `s`, False otherwise."



def test_4():

    main_doc, param_descriptions, return_doc = _parse_google_format_docstring(
        """
        Determines if two strings are anagrams by comparing character frequencies.

          Args:
              s (str): The first string used for comparison.
              t (str): The second string used for comparison.

          Returns:
              bool: True if `t` is an anagram of `s`, False otherwise.
        """)

    print(main_doc, param_descriptions, return_doc)

    assert main_doc.startswith("Determines if two strings are anagrams by comparing character frequencies.")
    assert param_descriptions == {'s': 'The first string used for comparison.', 't': 'The second string used for comparison.'}
    assert return_doc == "bool: True if `t` is an anagram of `s`, False otherwise."
