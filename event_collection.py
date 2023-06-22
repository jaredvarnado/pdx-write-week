from datetime import datetime
from bs4 import BeautifulSoup
import requests

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

def getBeautifulSoupParserFromUrl(url):
    return BeautifulSoup(requests.get(url).text, 'html.parser')

class RoseCityBookPub():
    # We can filter events by month.
    # currentDate = f"{datetime.now().strftime('%m')}-{datetime.now().year}"
    endpoint = 'https://www.rosecitybookpub.com'
    event_source = f'{endpoint}/events-1?view=list' # &month={currentDate}'
    at_rose_city_books = 'at Rose City Book Pub'

    def pull_events(self):
        print("Pulling events... " + self.event_source)
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

    def pull_events(self):
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
    #events = RoseCityBookPub().pull_events()
    #for e in events:
    #    print(e.getTitle())
    events = Powells().pull_events()
    events.extend(RoseCityBookPub().pull_events())
    for e in events:
        print(e.getTitle())


