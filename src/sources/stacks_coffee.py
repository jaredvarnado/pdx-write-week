import datetime
from event import Event
from utils import getBeautifulSoupParserFromUrl, formatDate, shouldIncludeEvent

class StacksCoffee():
    endpoint = 'https://www.thestackscoffeehouse.com'
    event_source_url = f'{endpoint}/events'
    at_bookstore = 'at the Stacks Coffeehouse'
    source_name = 'Stacks Coffeehouse'

    def pullEvents(self, period_start, period_end):
        results = []
        soup = getBeautifulSoupParserFromUrl(self.event_source_url)
        events = soup.find_all('div', {'class': 'eventlist-column-info'})
        for e in events:
            title_and_link = e.findChildren('a', {'class': 'eventlist-title-link'})[0]
            title = f'{title_and_link.get_text().strip()} {self.at_bookstore}'
            link = f"{self.endpoint}{title_and_link.get('href')}"
            date = e.findChildren('time', {'class': 'event-date'})[0].get('datetime')
            date = formatDate(datetime.datetime.strptime(date, '%Y-%m-%d').date())
            event_start = e.findChildren('time', {'class': 'event-time-12hr-start'})[0].get_text().strip()
            event_end= e.findChildren('time', {'class': 'event-time-12hr-end'})[0].get_text().strip()
            result = Event(title, date, event_start, event_end, link, self.source_name)
            if shouldIncludeEvent(result, period_start, period_end):
                results.append(result)

        return results
