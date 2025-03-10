

from smolagents._function_type_hints_utils import _parse_google_format_docstring




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
            function: the name of the function.
        """)
    print(main_doc, param_descriptions, return_doc)

    assert main_doc == "Update the docstring for the function."
    assert param_descriptions == {'docstring': 'A string containing the docstring for the function.', 'function': 'the name of the function.'}
    assert return_doc is None
