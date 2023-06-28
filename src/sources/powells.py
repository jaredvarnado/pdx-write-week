import datetime
from event import Event
from utils import getBeautifulSoupParserFromUrl, formatDate, shouldIncludeEvent

class Powells():
    source_name = 'Powells'
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
            result = Event(event_title, date_formated, start_time, None, link, self.source_name)
            if shouldIncludeEvent(result, period_start, period_end):
                results.append(result)
        return results
