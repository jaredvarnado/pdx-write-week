# pdx-write-week

### Dependencies

* Python 3.9 or higher: https://www.python.org/downloads/release/python-390/

* BeautifulSoup
```
pip install beautifulsoup4
```

* Jinja2

```
pip install Jinja2
```

### Scripts 

#### generate_report.py

Collects events from all sources, filters events by timespan (7 days of execution), and generates the html report to the current directory as `pdx-weekly-report-{{startDate}}-{{endDate}}.html`

