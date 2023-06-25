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

