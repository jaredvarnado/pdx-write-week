
import datetime
from event import Event
from utils import getBeautifulSoupParserFromUrl, formatDate, shouldIncludeEvent

class AnnieBloom():
    endpoint = 'https://www.annieblooms.com'
    event_source_url = f'{endpoint}/event/' # Might need to add date to url path (i.e. /2023-07)
    at_bookstore = 'at Annie Bloom\'s Books'
    def pullEvents(self, period_start, period_end):
        results = []
        start_month = period_start.month
        end_month = period_end.month
        soup = getBeautifulSoupParserFromUrl(self.event_source_url)
        events = soup.find_all('td', {'class': 'single-day future'})

        # If 7 day period crosses into next month,
        # we'll need to pull events from two month calendars.
        if start_month != end_month:
            next_month_param = f"{period_end.year}-{period_end.month}"
            soup_next_month = getBeautifulSoupParserFromUrl(f"{self.event_source_url}{next_month_param}")
            events.extend(soup_next_month.find_all('td', {'class': 'single-day future'}))

        for e in events:
            title = e.findChildren('div', {'class': 'views-field views-field-title'})[0].get_text().strip()
            title = f'{title} {self.at_bookstore}'
            date = e.findChildren('span', {'class': 'date-display-single'})[0].get_text().strip()
            date = date.split('-')[0].strip()
            event_start = e.findChildren('span', {'class': 'date-display-start'})[0].get_text().strip()
            event_end = e.findChildren('span', {'class': 'date-display-end'})[0].get_text().strip()
            link = f"{self.endpoint}{e.findChildren('a')[0].get('href')}"
            result = Event(title, date, event_start, event_end, link)
            if shouldIncludeEvent(result, period_start, period_end):
                results.append(result)

        return results