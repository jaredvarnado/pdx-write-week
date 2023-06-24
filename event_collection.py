#! /Library/Frameworks/Python.framework/Versions/3.9/bin/python3

# PDX Write Week
# https://us8.campaign-archive.com/home/?u=c5694bf7a3c233e034ad68e1c&id=6eafe29f11

import datetime
from bs4 import BeautifulSoup
import requests

## TODO: Sources to Add
# 1. [done] Mother Foucault's Bookshop - https://www.motherfoucaultsbookshop.com/calendar-list/stephen-thomas-teresa-k-miller
# 2. [done] Willamette Writers - https://willamettewriters.org/event/online-the-write-place-productivity-and-goal-setting/2023-06-22/
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

def formatDate(date):
    return date.strftime('%m/%d/%Y')

class WillametteWriters():

    endpoint = 'https://willamettewriters.org'
    event_source_url = f'{endpoint}/events/month/'
    will_writers = 'Willamette Writers'
    date_format = '%Y-%m-%d'

    def shouldIncludeEvent(self, event):
        if event.getTitle() == "Portland: Office Closed":
            return False
        return True

    def formatTitle(self, title):
        isVirtual = False
        isHybrid = False
        hybridSuffix = '(hybrid in person/virtual)'
        if title.startswith("Online:"):
            title = title[8:].strip() # cut out 'Online:'
            isVirtual = True
        elif title.startswith("Hybrid"):
            title = title[7:].strip()
            isHybrid = True
        if title.startswith("Hillsboro:"):
            title = title[10:].strip()
            title = f'{self.will_writers} Hillsboro Presents {title}'
        elif title.startswith("Eugene:"):
            title = title[7:].strip()
            title = f"{self.will_writers} Eugene Presents {title}"
        elif title.startswith("Salem"):
            title = title[6:].strip()
            title = f"{self.will_writers} Salem Presents {title}"
        elif title.startswith("Corvallis"):
            title = title[10:].strip()
            title = f"{self.will_writers} Corvallis Presents {title}"
        elif "Portland: Office Hours" == title:
            title = "Willamette Writers Portland Office Hours"
        elif title.startswith("Portland:"):
            title = title[10:].strip()
            title = f"{self.will_writers} Portland Presents {title}"
        else:
            title = f"{title} with Willamette Writers"
        if isVirtual == True:
            title = f"{title} (virtual)"
        if isHybrid == True:
            title = f"{title} {hybridSuffix}"
        return title

    def pullEvents(self, period_start, period_end):
        results = []
        soup = getBeautifulSoupParserFromUrl(self.event_source_url)
        days = soup.find_all('div', {'class': 'tribe-events-calendar-month-mobile-events__mobile-day'})
        for day in days:
            events = day.findChildren('article')
            for e in events:
                atag = e.findChildren('a', {'class': 'tribe-events-calendar-month-mobile-events__mobile-event-title-link tribe-common-anchor'})[0]
                link = atag.get('href')
                title = self.formatTitle(atag.get('title'))
                event_date = e.findChildren('time')[0].get('datetime')
                event_date_formated = formatDate(datetime.datetime.strptime(event_date, self.date_format).date())
                event_start = e.findChildren('span', {'class': 'tribe-event-date-start'})[0].get_text()
                event_start = event_start.split('@')[1].strip()
                event_end = e.findChildren('span', {'class': 'tribe-event-time'})[0].get_text()
                result = Event(title, event_date_formated, event_start, event_end, link)
                if self.shouldIncludeEvent(result) == True:
                    results.append(result)
        return results

class RoseCityBookPub():
    # We can filter events by month.
    # currentDate = f"{datetime.now().strftime('%m')}-{datetime.now().year}"
    endpoint = 'https://www.rosecitybookpub.com'
    event_source_url = f'{endpoint}/events-1?view=list' # &month={currentDate}'
    at_rose_city_books = 'at Rose City Book Pub'
    date_format = '%A, %B %d, %Y'

    def pullEvents(self, period_start, period_end):
        results = []
        soup = getBeautifulSoupParserFromUrl(self.event_source_url)
        events = soup.find_all('article', {'class': 'eventlist-event--upcoming'})
        for e in events:
            event_rel_link = e.findChildren('a', {'class': 'eventlist-title-link'})[0].get('href')
            event_abs_link = f'{self.endpoint}{event_rel_link}'
            event_title = e.findChildren('h1', {'class': 'eventlist-title'})[0].get_text()
            event_title = f'{event_title} {self.at_rose_city_books}'
            event_date = e.findChildren('time', {'class': 'event-date'})[0].get_text().strip()
            event_date_formated = formatDate(datetime.datetime.strptime(event_date, self.date_format).date())
            print(f"Converted Date From {event_date} -> {event_date_formated}")
            start_time = e.findChildren('time', {'class': 'event-time-12hr-start'})[0].get_text()
            end_time = e.findChildren('time', {'class': 'event-time-12hr-end'})[0].get_text()
            results.append(Event(event_title, event_date_formated, start_time, end_time, event_abs_link))
        return results

class Powells():
    endpoint = 'https://www.powells.com'
    event_source_url = f'{endpoint}/events-update'

    def pullEvents(self, period_start, period_end):
        results = []
        soup = getBeautifulSoupParserFromUrl(self.event_source_url)
        events = soup.find_all('div', {'class': 'bookwrapper'})
        for e in events:
            event_title = e.findChildren('h3')[0].get_text()

            text = e.findChildren('p')[0].get_text()
            date = text.split('/')[0].strip()
            location = text.split('/')[1].strip()
            event_title = f'{event_title} at {location}'

            start_time = date.split('@')[1].split('(')[0].strip()
            # Something to look out for - 
            # Powells' site does not include the Year (as of now).
            # This could cause a bug where calendar dates for next year begin (i.e. Jan 1)
            # we would be tacking on the current year to the end of it (i.e Jan 1, 2023 instead of 2024).
            date = date.split('@')[0].strip() + ', ' + str(datetime.datetime.now().year)
            date_formated = formatDate(datetime.datetime.strptime(date, '%A, %B %d, %Y').date())

            link = e.findChildren('a')[0].get('href')
            link = f'{self.endpoint}{link}'
            results.append(Event(event_title, date_formated, start_time, None, link))
        return results


class MotherFoucaults():
    endpoint = 'https://www.motherfoucaultsbookshop.com'
    event_source_url = f'{endpoint}/calendar-list/'
    at_bookshop = 'at Mother Foucault\'s Bookshop'

    # Mother F's contains events like "<Month> OPP"
    # with no description of said event.
    # TODO: May need to filter these events out if they are not
    # reading/writing related.

    def pullEvents(self, period_start, period_end):
        results = []
        soup = getBeautifulSoupParserFromUrl(self.event_source_url)
        events = soup.find_all('article', {'class': 'eventlist-event eventlist-event--upcoming'})
        for e in events:
            title = e.findChildren('h1', {'class': 'eventlist-title'})[0].get_text()
            title = f'{title} {self.at_bookshop}'
            event_date = e.findChildren('time', {'class': 'event-date'})[0].get('datetime')
            event_date_formated = formatDate(datetime.datetime.strptime(event_date, '%Y-%m-%d').date())
            event_start = e.findChildren('time', {'class': 'event-time-localized-start'})[0].get_text()
            event_end = e.findChildren('time', {'class': 'event-time-localized-end'})[0].get_text()
            link = e.findChildren('a', {'class': 'eventlist-title-link'})[0].get('href')
            link = f'{self.endpoint}{link}'
            results.append(Event(title, event_date_formated, event_start, event_end, link))
        return results

class AnnieBloom():
    endpoint = 'https://www.annieblooms.com'
    event_source_url = f'{endpoint}/event/' # Might need to add date to url path (i.e. /2023-07)

    def pullEvents(self, period_start, period_end):
        results = []
        start_month = today.month
        end_month = week_from_now.month
        soup = getBeautifulSoupParserFromUrl(self.event_source_url)
        events = soup.find_all('td', {'class': 'single-day future'})

        # If 7 day period crosses into next month,
        # we'll need to pull events from two month calendars.
        if start_month != end_month:
            next_month_param = f"{week_from_now.year}-{week_from_now.month}"
            soup_next_month = getBeautifulSoupParserFromUrl(f"{self.event_source_url}{next_month_param}")
            events.extend(soup_next_month.find_all('td', {'class': 'single-day future'}))

        for e in events:
            title = e.findChildren('div', {'class': 'views-field views-field-title'})[0].get_text()
            print(title)

        return results

if __name__ == "__main__":
    today = datetime.datetime.now()
    week_from_now = today + datetime.timedelta(days=7)
    print(f'Pulling events from {today} to {week_from_now}')
    sources  = [ MotherFoucaults(), RoseCityBookPub(), Powells(), WillametteWriters() ]
    #sources = [ AnnieBloom() ]
    events = []
    for source in sources:
        events.extend(source.pullEvents(today, week_from_now))
    for event in events:
        print(event.toString())
