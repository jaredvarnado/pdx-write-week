#! /Library/Frameworks/Python.framework/Versions/3.9/bin/python3

# PDX Write Week
# https://us8.campaign-archive.com/home/?u=c5694bf7a3c233e034ad68e1c&id=6eafe29f11

import datetime

from sources.annie_bloom import AnnieBloom
from sources.literary_arts import LiteraryArts
from sources.mother_foucaults import MotherFoucaults
from sources.powells import Powells
from sources.rosecity import RoseCityBookPub
from sources.stacks_coffee import StacksCoffee
from sources.willamette_writers import WillametteWriters

EVENT_TIME_WINDOW_IN_DAYS = 7

# Currently support the following event sources:
# 1. Mother Foucault's Bookshop - https://www.motherfoucaultsbookshop.com/calendar-list/stephen-thomas-teresa-k-miller
# 2. Willamette Writers - https://willamettewriters.org/event/online-the-write-place-productivity-and-goal-setting/2023-06-22/
# 3. Annie Blooms - https://www.annieblooms.com/event/reading-zaji-cox-plums-months
# 4. The Stacks Coffeehouse - https://www.thestackscoffeehouse.com/writingcafe
# 5. Literary Arts - (may need to filter type of event?) https://literary-arts.org/event 

# TODO: Remove duplicate events from list
if __name__ == "__main__":
    today = datetime.datetime.now()
    week_from_now = today + datetime.timedelta(days=EVENT_TIME_WINDOW_IN_DAYS)

    print(f'Pulling events from {today} to {week_from_now}')
    sources  = [ LiteraryArts(), AnnieBloom(), MotherFoucaults(), RoseCityBookPub(), Powells(), WillametteWriters(), StacksCoffee() ]

    events = []
    for source in sources:
        events.extend(source.pullEvents(today, week_from_now))

    # Sort events by date
    events.sort(key=lambda x: x.date)

    for event in events:
        print(event.toString())
