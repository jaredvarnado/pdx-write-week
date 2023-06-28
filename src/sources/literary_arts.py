import datetime
from event import Event
from utils import getBeautifulSoupParserFromUrl, formatDate, shouldIncludeEvent

class LiteraryArts():
    endpoint = 'https://literary-arts.org'
    event_source_url = f'{endpoint}/event'
    at_arts = 'at Literary Arts'
    source_name = 'Literary Arts'
    tuition_required = '(tuition required)'
    virtual = '(virtual)'

    def pullEvents(self, period_start, period_end):
        results = []
        soup = getBeautifulSoupParserFromUrl(self.event_source_url)
        events = soup.find_all('div', {'class': 'tribe-common-g-row tribe-events-calendar-list__event-row'})
        for e in events:
            event_date = e.findChildren('time', {'class': 'tribe-events-calendar-list__event-datetime'})[0].get('datetime')
            event_date = formatDate(datetime.datetime.strptime(event_date, '%Y-%m-%d').date())
            event_start = e.findChildren('span', {'class': 'tribe-event-date-start'})[0].get_text().split('from')[1].strip()
            event_end = e.findChildren('span', {'class': 'tribe-event-time'})[0].get_text().strip()
            title_upper_case = e.findChildren('h3', {'class': 'tribe-events-list-event-title'})[0]
            title = title_upper_case.findChildren('a')[0].get('title')
            title = f'{title} {self.at_arts}'
        
            link = title_upper_case.findChildren('a')[0].get('href')
            tags = e.findChildren('header', {'class': 'tribe-events-calendar-list__event-header'})
            added_virt = False
            added_tu = False
            for tag in tags:
                if "writing classes" in tag.get_text().strip().lower():
                    if added_tu == False:
                        title = f'{title} {self.tuition_required}'
                        added_tu = True
                if "online" in tag.get_text().strip().lower():
                    if added_virt == False:
                        title = f'{title} {self.virtual}'
                        added_virt = True

            result = Event(title, event_date, event_start, event_end, link, self.source_name)
            if shouldIncludeEvent(result, period_start, period_end):
                results.append(result)
        return results
