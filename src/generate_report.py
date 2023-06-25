# Warning: you'll likely need to change this line to your local python path
#! /Library/Frameworks/Python.framework/Versions/3.9/bin/python3

# PDX Write Week
# https://us8.campaign-archive.com/home/?u=c5694bf7a3c233e034ad68e1c&id=6eafe29f11

import datetime

from sources.annie_bloom import AnnieBloom
from sources.broadway_books import BroadwayBooks
from sources.literary_arts import LiteraryArts
from sources.mother_foucaults import MotherFoucaults
from sources.powells import Powells
from sources.rosecity import RoseCityBookPub
from sources.stacks_coffee import StacksCoffee
from sources.willamette_writers import WillametteWriters
from utils import formatDate
from generate_templates import generate_html_doc, write_html_doc

EVENT_TIME_WINDOW_IN_DAYS = 7

# TODO: Remove duplicate events from list
if __name__ == "__main__":
    today = datetime.datetime.now()
    report_end_date = today + datetime.timedelta(days=EVENT_TIME_WINDOW_IN_DAYS)

    print(f'Pulling events from {today} to {report_end_date}')
    sources  = [ BroadwayBooks(), LiteraryArts(), AnnieBloom(), MotherFoucaults(), RoseCityBookPub(), Powells(), WillametteWriters(), StacksCoffee() ]
    events = []
    for source in sources:
        print(f'Requesting events from [{source.endpoint}]')
        results = source.pullEvents(today, report_end_date)
        print(f'Found {str(len(results))} events')
        events.extend(results)

    # Sort events by date
    events.sort(key=lambda x: x.date)

    report = generate_html_doc(formatDate(today), formatDate(report_end_date), events)
    out_file = f"./pdx-weekly-report-{today.strftime('%Y%m%d')}-{report_end_date.strftime('%Y%m%d')}.html"
    write_html_doc(out_file, report)