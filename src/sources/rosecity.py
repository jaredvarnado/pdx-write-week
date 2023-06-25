import datetime
from event import Event
from utils import getBeautifulSoupParserFromUrl, formatDate, shouldIncludeEvent

class RoseCityBookPub():
    # We can filter events by month.
    # currentDate = f"{datetime.now().strftime('%m')}-{datetime.now().year}"
    # However RCB Events page includes all upcoming events by default.
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
            start_time = e.findChildren('time', {'class': 'event-time-12hr-start'})[0].get_text()
            end_time = e.findChildren('time', {'class': 'event-time-12hr-end'})[0].get_text()
            result = Event(event_title, event_date_formated, start_time, end_time, event_abs_link)
            if shouldIncludeEvent(result, period_start, period_end):
                results.append(result)
        return results