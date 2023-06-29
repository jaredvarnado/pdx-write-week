# Warning: you'll likely need to change this line to your local python path
#! /Library/Frameworks/Python.framework/Versions/3.9/bin/python3

# PDX Write Week
# https://us8.campaign-archive.com/home/?u=c5694bf7a3c233e034ad68e1c&id=6eafe29f11

import datetime
import argparse

from sources.annie_bloom import AnnieBloom
from sources.broadway_books import BroadwayBooks
from sources.literary_arts import LiteraryArts
from sources.mother_foucaults import MotherFoucaults
from sources.powells import Powells
from sources.rosecity import RoseCityBookPub
from sources.stacks_coffee import StacksCoffee
from sources.willamette_writers import WillametteWriters
from utils import formatDate
from generate_templates import generate_csv, generate_html

EVENT_TIME_WINDOW_IN_DAYS = 7

parser = argparse.ArgumentParser(description='Generate Report will generate a report.')
parser.add_argument('--one-week', action='store_true',
                    help='Pull events for only the next week.')
parser.add_argument('--output', help='Type of output [ html, csv ]. Defaults to csv.')

if __name__ == "__main__":
    args = parser.parse_args()

    output_type = args.output if args.output is not None else 'csv'
    output_type = output_type.lower()
    if output_type not in [ 'csv', 'html' ]:
        raise Exception("Output can only be [ csv ] or [ html ]")

    today = datetime.datetime.now()
    if args.one_week:
        report_end_date = today + datetime.timedelta(days=EVENT_TIME_WINDOW_IN_DAYS)
        print(f'Pulling events from {today} to {report_end_date}')
    else:
        report_end_date = today + datetime.timedelta(days=120)
        print('Pulling all upcoming events.')

    sources  = [ BroadwayBooks(), LiteraryArts(), AnnieBloom(), MotherFoucaults(), RoseCityBookPub(), Powells(), WillametteWriters(), StacksCoffee() ]
    events = []
    for source in sources:
        results = []
        print(f'Requesting events from [{source.endpoint}]')
        results = source.pullEvents(today, report_end_date)
        events.extend(results)

    # Sort events by date
    events.sort(key=lambda x: x.date)

    unique_events = { e for e in events }
    out_file = 'pdx-weekly-report'
    if args.one_week:
        out_file = f"{out_file}-{today.strftime('%Y%m%d')}-{report_end_date.strftime('%Y%m%d')}.{output_type}"
    else:
        out_file = f"{out_file}-{today.strftime('%Y%m%d')}.{output_type}"

    if output_type == 'html':
        generate_html(out_file, formatDate(today), formatDate(report_end_date), unique_events)
    else:
        generate_csv(out_file, unique_events)