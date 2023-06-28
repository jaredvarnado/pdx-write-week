from bs4 import BeautifulSoup
import requests
import datetime

def getBeautifulSoupParserFromUrl(url):
    return BeautifulSoup(requests.get(url).text, 'html.parser')

def formatDate(date):
    return date.strftime('%m/%d/%Y')

def shouldIncludeEvent(event, start_date, end_date):
    if event.getTitle() == "Portland: Office Closed":
        return False
    event_date = datetime.datetime.strptime(event.getDate(), '%m/%d/%Y')
    if event_date < start_date:
        return False
    if event_date > end_date:
        return False
    return True

def getDifferenceBetweenDatesInMonths(d1, d2):
    return (d1.year - d2.year) * 12 + d1.month - d2.month

def getMonthsBetweenDates(end, start):
    loop_break = 0
    loop_max = 100 # Stop infinite loops from happening

    end_date_str = f"{end.year}-{end.strftime('%m')}"
    start_date_str = f"{start.year}-{start.strftime('%m')}"
    start_month = start.strftime('%m')
    start_year = start.year

    months = [ start_date_str ]
    while start_date_str != end_date_str:
        loop_break = loop_break + 1
        if loop_break > loop_max:
            raise Exception(f'Possible infinite loop detected - breaking thread! Check calendar dates passed to getMonthsBetweenDates method [{end}] [{start}]')
        if start_month == '12':
            start_month = '1'
            start_year = start_year + 1
        else:
            start_month = str(int(start_month) + 1)
        if int(start_month) < 10:
            start_month = f'0{str(start_month)}'

        start_date_str = f'{start_year}-{start_month}'
        months.append(start_date_str)

    return months