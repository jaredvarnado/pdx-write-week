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

from generate_templates import print_html_doc

EVENT_TIME_WINDOW_IN_DAYS = 7

# TODO: Remove duplicate events from list
if __name__ == "__main__":
    today = datetime.datetime.now()
    week_from_now = today + datetime.timedelta(days=EVENT_TIME_WINDOW_IN_DAYS)

    print(f'Pulling events from {today} to {week_from_now}')
    sources  = [ BroadwayBooks(), LiteraryArts(), AnnieBloom(), MotherFoucaults(), RoseCityBookPub(), Powells(), WillametteWriters(), StacksCoffee() ]

    events = []
    for source in sources:
        events.extend(source.pullEvents(today, week_from_now))

    # Sort events by date
    events.sort(key=lambda x: x.date)

    print_html_doc(events)
