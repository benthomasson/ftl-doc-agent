import os
import yaml


def generate_python_header(
    output, problem, tools_files, tools,
):

    with open(output, "w") as f:
        f.write("#!/usr/bin/env python3\n")
        if problem:
            f.write(f'Problem:{problem}\n')
        f.write('"""\n')
        f.write("import ftl_pytest_agent\n")
        f.write("import os\n\n\n")
        f.write("with ftl_pytest_agent.automation(\n")
        f.write(f"tools_files={tools_files},\n")
        f.write(f"tools={tools},\n")
        f.write(") as ftl:\n\n")

        for t in tools:
            f.write(f"    {t} = ftl.tools.{t}\n")

        f.write("\n")


def generate_python_tool_call(output, call):
    with open(output, "a") as f:
        f.write("\n    ")
        f.write("\n    ".join(call.arguments.strip().split("\n")))
        f.write("\n")


def reformat_python(output):
    os.system("black " + output)


def generate_explain_header(explain, problem):
    with open(explain, "w") as f:
        if problem:
            f.write("Problem: {problem}\n\n")


def generate_explain_action_step(explain, o):
    if o.model_output:
        with open(explain, "a") as f:
            f.write(f"Step {o.step_number:2d} ")
            f.write("-" * 100)
            f.write("\n\n")
            f.write(o.model_output)
            f.write("\n\n")
