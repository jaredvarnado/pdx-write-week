#! /Library/Frameworks/Python.framework/Versions/3.9/bin/python3
import os
import csv
from event import Event
from jinja2 import Environment, FileSystemLoader

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
TABLE_TEMPLATE_FILE = f"{THIS_DIR}/templates/event_table.template.jinja"

CSV_FIELDS = ['Event', 'Description', 'Date', 'Link', 'Source', 'Week Number']

def generate_csv(out_file, events):
    with open(out_file, 'w', encoding='utf-8') as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(CSV_FIELDS)
        for e in events:
            csvwriter.writerow(e.toRow())

def generate_html(out_file, startTime, endTime, events):
    # Create the jinja2 environment.
    # Notice the use of trim_blocks, which greatly helps control whitespace.
    j2_env = Environment(loader=FileSystemLoader(THIS_DIR),
                         trim_blocks=True)
    html = j2_env.get_template('./templates/event_table.template.jinja').render(
        startTime=startTime,
        endTime=endTime,
        events=events
    )

    with open(out_file, 'w', encoding='utf-8') as f:
        f.write(html)
