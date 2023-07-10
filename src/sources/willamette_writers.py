import datetime
from event import Event
from utils import getBeautifulSoupParserFromUrl, getDifferenceBetweenDatesInMonths, getMonthsBetweenDates, formatDate, shouldIncludeEvent

class WillametteWriters():

    endpoint = 'https://willamettewriters.org'
    event_source_url = f'{endpoint}/events/month/'
    will_writers = 'Willamette Writers'
    date_format = '%Y-%m-%d'

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
        start_month = period_start.month
        end_month = period_end.month
        soup = getBeautifulSoupParserFromUrl(self.event_source_url)
        days = soup.find_all('div', {'class': 'tribe-events-calendar-month-mobile-events__mobile-day'})

        if getDifferenceBetweenDatesInMonths(period_start, period_end) != 0:
            for m in getMonthsBetweenDates(period_end, period_start):
                month_url = f'{self.event_source_url}{m}/'
                print(f"Making extra call to [ {month_url} ]")
                soup_next_month = getBeautifulSoupParserFromUrl(f'{month_url}')
                days.extend(soup.find_all('div', {'class': 'tribe-events-calendar-month-mobile-events__mobile-day'}))

        for day in days:
            events = day.findChildren('article')
            for e in events:
                atag = e.findChildren('a', {'class': 'tribe-events-calendar-month-mobile-events__mobile-event-title-link tribe-common-anchor'})[0]
                link = atag.get('href')
                title = self.formatTitle(atag.get('title'))
                event_date = e.findChildren('time')[0].get('datetime')
                event_date_formated = formatDate(datetime.datetime.strptime(event_date, self.date_format).date())

                event_start = e.findChildren('span', {'class': 'tribe-event-date-start'})
                if len(event_start) > 0:
                    event_start = event_start[0].get_text().split('@')[1].strip()
                    event_end = e.findChildren('span', {'class': 'tribe-event-time'})[0].get_text()
                else:
                    event_start = e.findChildren('div', {'class': 'tribe-events-calendar-month-mobile-events__mobile-event-datetime'})[0].get_text().strip()
                    event_end = None

                result = Event(title, event_date_formated, event_start, event_end, link, self.will_writers)
                if shouldIncludeEvent(result, period_start, period_end):
                    results.append(result)
        return results
