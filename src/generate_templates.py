#! /Library/Frameworks/Python.framework/Versions/3.9/bin/python3
import os
from jinja2 import Environment, FileSystemLoader

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
TABLE_TEMPLATE_FILE = f"{THIS_DIR}/templates/event_table.template.jinja"

def print_html_doc(events):
    # Create the jinja2 environment.
    # Notice the use of trim_blocks, which greatly helps control whitespace.
    j2_env = Environment(loader=FileSystemLoader(THIS_DIR),
                         trim_blocks=True)
    print(j2_env.get_template('./templates/event_table.template.jinja').render(
        events=events
    ))
