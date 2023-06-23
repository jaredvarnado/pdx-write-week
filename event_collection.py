#! /Library/Frameworks/Python.framework/Versions/3.9/bin/python3

from datetime import datetime
from bs4 import BeautifulSoup
import requests

## TODO: Sources to Add
# 1. Mother Foucault's Bookshop - https://www.motherfoucaultsbookshop.com/calendar-list/stephen-thomas-teresa-k-miller
# 2. Willamette Writers - https://willamettewriters.org/event/online-the-write-place-productivity-and-goal-setting/2023-06-22/
# 3. Annie Blooms - https://www.annieblooms.com/event/reading-zaji-cox-plums-months
# 4. The Stacks Coffeehouse - https://www.thestackscoffeehouse.com/writingcafe
# 5. Literary Arts - (may need to filter type of event?) https://literary-arts.org/event 

## TODO: Filter all events by date range
# * Determine beginning and end dates for time range (1 week/2 weeks?)
# * Format date of event into timestamp to use for comparison operations.
# * if event_timestamp is between timerange_start and timerange_end -> include event.

class Event:
    def __init__(self, title, date, startTime, endTime, link):
        self.title = title
        self.date = date
        self.startTime = startTime
        self.endTime = endTime
        self.link = link
    def getTitle(self):
        return self.title
    def getDate(self):
        return self.date
    def getStartTime(self):
        return self.startTime
    def getEndTime(self):
        return self.endTime
    def getLink(self):
        return self.link
    def toString(self):
        return f"{self.title},{self.date},{self.startTime},{self.endTime},{self.link}"

def getBeautifulSoupParserFromUrl(url):
    return BeautifulSoup(requests.get(url).text, 'html.parser')

class WillametteWriters():

    endpoint = 'https://willamettewriters.org'
    event_source = f'{endpoint}/events/month/'

    def pullEvents(self):
        results = []
        soup = getBeautifulSoupParserFromUrl(self.event_source)
        days = soup.find_all('div', {'class': 'tribe-events-calendar-month-mobile-events__mobile-day'})
        for day in days:
            #print(day)
            events = day.findChildren('article')
            for e in events:
                atag = e.findChildren('a', {'class': 'tribe-events-calendar-month-mobile-events__mobile-event-title-link tribe-common-anchor'})[0]
                link = atag.get('href')
                title = atag.get('title')
                if title.startswith("Online:"):
                    title = title[8:] # cut out 'Online:'
                    title = f'{title} (virtual)' # add virtual suffix
                if "Portland: Office Hours" == title:
                    title = "Willamette Writers Portland Office Hours"
                event_date = e.findChildren('time')[0].get('datetime')
                event_start = e.findChildren('span', {'class': 'tribe-event-date-start'})[0].get_text()
                event_end = e.findChildren('span', {'class': 'tribe-event-time'})[0].get_text()
                results.append(Event(title, event_date, event_start, event_end, link))
        return results

class RoseCityBookPub():
    # We can filter events by month.
    # currentDate = f"{datetime.now().strftime('%m')}-{datetime.now().year}"
    endpoint = 'https://www.rosecitybookpub.com'
    event_source = f'{endpoint}/events-1?view=list' # &month={currentDate}'
    at_rose_city_books = 'at Rose City Book Pub'

    def pullEvents(self):
        results = []
        soup = getBeautifulSoupParserFromUrl(self.event_source)
        events = soup.find_all('article', {'class': 'eventlist-event--upcoming'})
        for e in events:
            event_rel_link = e.findChildren('a', {'class': 'eventlist-title-link'})[0].get('href')
            event_abs_link = f'{self.endpoint}{event_rel_link}'
            event_title = e.findChildren('h1', {'class': 'eventlist-title'})[0].get_text()
            event_title = f'{event_title} {self.at_rose_city_books}'
            event_date = e.findChildren('time', {'class': 'event-date'})[0].get_text()
            start_time = e.findChildren('time', {'class': 'event-time-12hr-start'})[0].get_text()
            end_time = e.findChildren('time', {'class': 'event-time-12hr-end'})[0].get_text()
            results.append(Event(event_title, event_date, start_time, end_time, event_abs_link))
        return results

class Powells():
    endpoint = 'https://www.powells.com'
    event_source = f'{endpoint}/events-update'

    def pullEvents(self):
        results = []
        soup = getBeautifulSoupParserFromUrl(self.event_source)
        events = soup.find_all('div', {'class': 'bookwrapper'})
        for e in events:
            event_title = e.findChildren('h3')[0].get_text()

            text = e.findChildren('p')[0].get_text()
            date = text.split('/')[0].strip()
            location = text.split('/')[1].strip()
            event_title = f'{event_title} at {location}'

            start_time = date.split('@')[1].split('(')[0].strip()
            date = date.split('@')[0].strip()

            link = e.findChildren('a')[0].get('href')
            link = f'{self.endpoint}{link}'
            results.append(Event(event_title, date, start_time, None, link))
        return results


if __name__ == "__main__":
    sources  = [ RoseCityBookPub(), Powells(), WillametteWriters() ]
    events = []
    for source in sources:
        events.extend(source.pullEvents())
    for event in events:
        print(event.toString())
