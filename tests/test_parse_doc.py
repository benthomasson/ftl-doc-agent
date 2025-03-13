from ftl_doc_agent.tools import _convert_type_hints_to_json_schema

import re
import json


from _function_type_hints_utils import _parse_google_format_docstring, DocstringParsingException


def parse_and_check_docstring(func, docstring):

    main_doc, param_descriptions, return_doc = _parse_google_format_docstring(docstring)
    json_schema = _convert_type_hints_to_json_schema(func)
    if (return_dict := json_schema["properties"].pop("return", None)) is not None:
        if (
            return_doc is not None
        ):  # We allow a missing return docstring since most templates ignore it
            return_dict["description"] = return_doc
    else:
        return_dict = {}
    for arg, schema in json_schema["properties"].items():
        if "arg" == "self":
            continue
        if arg not in param_descriptions:
            raise DocstringParsingException(
                f"Cannot generate JSON schema for {func.__name__} because the docstring has no description for the argument '{arg}'"
            )
        desc = param_descriptions[arg]
        enum_choices = re.search(r"\(choices:\s*(.*?)\)\s*$", desc, flags=re.IGNORECASE)
        if enum_choices:
            schema["enum"] = [c.strip() for c in json.loads(enum_choices.group(1))]
            desc = enum_choices.string[: enum_choices.start()].strip()
        schema["description"] = desc


def test_1():

    docstring = """
      Determines if a given string `s` matches a specified pattern of characters.

      The function verifies whether the structure of words in `s` aligns with the character sequence defined by `pattern`. Each unique
  character in `pattern` must correspond to a distinct word in `s`, and vice versa, maintaining consistency throughout.

      Args:
          pattern: A string representing the character pattern to match.
          s: The input string whose structure is to be validated against the pattern.

      Returns:
          bool: True if `s` follows the specified pattern, False otherwise.
      """

    def fn(pattern: str, s: str) -> bool:
        pass

    parse_and_check_docstring(fn, docstring)


def test_2():
    docstring = """

    Determines the position of the pillow after 'time' seconds in a line of 'n' people passing it sequentially in both directions.

    Args:
        n: Number of people standing in a line (int)
        time: Number of seconds the pillow has been passed (int)

    Returns:
        The index (starting from 1) of the person holding the pillow after 'time' seconds (int)
    """

    def fn(n: int, time: int) -> int:
        pass

    parse_and_check_docstring(fn, docstring)


def test_3():

    docstring = """
  Determines which person holds the pillow after 'time' seconds in a line of 'n' people passing it back and forth.

  Args:
      n (int): Number of people standing in a straight line. Must be >= 2.
          Example: For n=4, there are four people numbered from 1 to 4.
      time (int): Number of seconds the pillow has been passed. Must be >= 1.
          Example: For time=5, the pillow has changed hands five times.

  Returns:
      int: The index of the person currently holding the pillow after 'time' seconds.

  Example:
      Input: n=4, time=5
      Output: 2
      Explanation: The sequence is 1 -> 2 -> 3 -> 4 -> 3 -> 2.
  """

    def fn(n: int, time: int) -> int:
        pass

    parse_and_check_docstring(fn, docstring)
