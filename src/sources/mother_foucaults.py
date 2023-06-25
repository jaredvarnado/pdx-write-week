import datetime
from event import Event
from utils import getBeautifulSoupParserFromUrl, formatDate, shouldIncludeEvent


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
            result = Event(title, event_date_formated, event_start, event_end, link)
            if shouldIncludeEvent(result, period_start, period_end):
                results.append(result)
        return results