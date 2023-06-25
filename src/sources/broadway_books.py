
import datetime
from event import Event
from utils import getBeautifulSoupParserFromUrl, formatDate, shouldIncludeEvent


# Broadways site has dynamic mouse-over events
# which contain the event start/end times.
# We will need to use a headless browser like selenium to extract this data
# See https://stackoverflow.com/questions/62469332/using-selenium-and-python-to-extract-data-when-it-pops-up-after-mouse-hover
# For now, we will continue without start/end times for each event.
class BroadwayBooks():
    endpoint = 'https://www.broadwaybooks.net'
    event_source_url = f'{endpoint}/event/'
    at_bookstore = 'at Broadway Books'
    def pullEvents(self, period_start, period_end):
        results = []
        start_month = period_start.month
        end_month = period_end.month
        soup = getBeautifulSoupParserFromUrl(self.event_source_url)
        events = soup.find_all('td', {'class': 'single-day future'})

        # If 7 day period crosses into next month,
        # we'll need to pull events from two month calendars.
        # URL Path paramtere is `/event/2023-07` {Year}-{Month}
        if start_month != end_month:
            next_month_param = f"{period_end.year}-{period_end.month}"
            soup_next_month = getBeautifulSoupParserFromUrl(f"{self.event_source_url}{next_month_param}")
            events.extend(soup_next_month.find_all('td', {'class': 'single-day future'}))

        for e in events:
            title = e.findChildren('div', {'class': 'views-field-title'})[0].get_text().strip()
            title = f'{title} {self.at_bookstore}'
            event_date = formatDate(datetime.datetime.strptime(e.get('data-date'), '%Y-%m-%d').date())
            link = f"{self.endpoint}{e.findChildren('a')[0].get('href')}"
            result = Event(title, event_date, None, None, link)
            if shouldIncludeEvent(result, period_start, period_end):
                results.append(result)

        return results