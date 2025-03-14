import click

from .core import create_model, run_agent
from .default_tools import TOOLS3
from .tools import get_tool
from .codegen import (
    generate_explain_header,
    generate_explain_action_step,
    reformat_python,
)
from ftl_doc_agent.memory import ActionStep
from smolagents.agent_types import AgentText
from .util import get_functions, get_function_code

from redbaron import RedBaron
from pprint import pprint


@click.command()
@click.argument("code-file")
@click.argument("function")
@click.option("--model", "-m", default="ollama_chat/deepseek-r1:14b")
@click.option("--output", "-o", default="output.py")
@click.option("--explain", "-e", default="output.txt")
def main(
    code_file,
    function,
    model,
    output,
    explain,
):
    """An agent that updates code with type hints"""

    tool_classes = {}
    tool_classes.update(TOOLS3)
    model = create_model(model)
    state = {
        'func': None,
    }

    tools = ['complete']

    module, fns = get_functions(code_file)

    fn = state['func'] = getattr(module, function)
    function_code = get_function_code(fn)

    prompt = f"""Given the definition of the following python function create a function signature that
includes type hints for the function parameters and the return value.  Be sure to give your signature
in a python code blob.

Finally call complete() when done to signal you have completed the task.

The function:
{function_code}

    """

    generate_explain_header(explain, prompt)

    code_blocks = []
    imports = []

    for o in run_agent(
        tools=[get_tool(tool_classes, t, state) for t in tools],
        model=model,
        problem_statement=prompt,
    ):
        if isinstance(o, ActionStep):
            generate_explain_action_step(explain, o)
            if o.trace and o.tool_calls:
                for call in o.tool_calls:
                    code_blocks.append(call.arguments)
        elif isinstance(o, AgentText):
            print(o.to_string())

    # print(code_blocks)
    with open(code_file) as f:
        red = RedBaron(f.read())

    target = None
    for o in red:
        if o.name == function and o.type == "def":
            target = o
            break

    if target is None:
        raise Exception(f'function {function} not found in code')

    found = False
    for code_block in code_blocks:
        # print(code_block)
        red_fn = RedBaron(code_block)
        # red_fn.help()
        for o in red_fn:
            if o.name == function and o.type == "def":
                # replace the fn body with the target fn body
                o.value = target.value
                # replace the whole fn with the fn with type hints
                target.replace(o)
                found = True
            if o.type == "from_import":
                imports.append(o)
            if o.type == "import":
                imports.append(o)
        else:
            continue
        break

    if not found:
        pprint(code_blocks)
        raise Exception(f'function {function} not found in code blocks')

    for imp in imports:
        red.insert(0, imp)

    print(target.dumps())

    # print(state['docstring'])
    # red[0].value.insert(0, f'\n"""{state["docstring"]}"""\n')
    # pprint(red.dumps())

    with open(output, 'w') as f:
        f.write(red.dumps())
        # print(red.dumps())

    reformat_python(output)
