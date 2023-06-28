
import datetime
from event import Event
from utils import getBeautifulSoupParserFromUrl, getDifferenceBetweenDatesInMonths, getMonthsBetweenDates, formatDate, shouldIncludeEvent

class AnnieBloom():
    endpoint = 'https://www.annieblooms.com'
    event_source_url = f'{endpoint}/event/' # Might need to add date to url path (i.e. /2023-07)
    at_bookstore = 'at Annie Bloom\'s Books'
    source_name = 'Annie Bloom\'s Books'

    def pullEvents(self, period_start, period_end):
        results = []
        start_month = period_start.month
        end_month = period_end.month
        soup = getBeautifulSoupParserFromUrl(self.event_source_url)
        events = soup.find_all('td', {'class': 'single-day future'})


        # TODO: Annie Blooms isn't pulling events. Find out why!

        # If 7 day period crosses into next month,
        # we'll need to pull events from two month calendars.
        if getDifferenceBetweenDatesInMonths(period_start, period_end) != 0:
            for m in getMonthsBetweenDates(period_end, period_start):
                month_url = f'{self.event_source_url}{m}'
                print(f"Making extra call to [ {month_url} ]")
                soup_next_month = getBeautifulSoupParserFromUrl(f'{month_url}')
                events.extend(soup_next_month.find_all('td', {'class': 'single-day future'}))

        for e in events:
            title = e.findChildren('div', {'class': 'views-field views-field-title'})[0].get_text().strip()
            title = f'{title} {self.at_bookstore}'
            date = e.findChildren('span', {'class': 'date-display-single'})[0].get_text().strip()
            date = date.split('-')[0].strip()
            event_start = e.findChildren('span', {'class': 'date-display-start'})[0].get_text().strip()
            event_end = e.findChildren('span', {'class': 'date-display-end'})[0].get_text().strip()
            link = f"{self.endpoint}{e.findChildren('a')[0].get('href')}"
            result = Event(title, date, event_start, event_end, link, self.source_name)
            if shouldIncludeEvent(result, period_start, period_end):
                results.append(result)

        return results