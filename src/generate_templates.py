#! /Library/Frameworks/Python.framework/Versions/3.9/bin/python3
import os
from jinja2 import Environment, FileSystemLoader

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
TABLE_TEMPLATE_FILE = f"{THIS_DIR}/templates/event_table.template.jinja"

def generate_html_doc(startTime, endTime, events):
    # Create the jinja2 environment.
    # Notice the use of trim_blocks, which greatly helps control whitespace.
    j2_env = Environment(loader=FileSystemLoader(THIS_DIR),
                         trim_blocks=True)
    return j2_env.get_template('./templates/event_table.template.jinja').render(
        startTime=startTime,
        endTime=endTime,
        events=events
    )

def write_html_doc(out_file, html):
    with open(out_file, 'w') as f:
        f.write(html)
