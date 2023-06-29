from datetime import datetime

class Event:
    def __init__(self, title, date, startTime, endTime, link, source):
        self.title = title.replace('"', '')
        self.date = date
        self.startTime = startTime
        self.endTime = endTime
        self.link = link
        self.source = source
        if self.startTime is not None:
            self.startTime = self.startTime.replace(" ", "")
        if self.endTime is not None:
            self.endTime = self.endTime.replace(" ", "")

    def __eq__(self, other):
        if not isinstance(other, Event):
            return NotImplemented
        return self.title == other.title and self.date == other.date and self.startTime == other.startTime and self.endTime == other.endTime and self.link == other.link and self.source == other.source

    def __hash__(self):
        return hash((self.title, self.date, self.link, self.source, self.endTime, self.startTime))

    def getTitle(self):
        return self.title
    def getDate(self):
        return self.date
    def getStartTime(self):
        return self.startTime
    def getEndTime(self):
        return self.endTime
    def getLink(self):
        return self.link
    def getSource(self):
        return self.source

    def toRow(self):
        description = ''
        if self.startTime is not None:
            if self.endTime is not None:
                description = f'{self.startTime} - {self.endTime}'
            else:
                description = f'{self.startTime}'
        return [ self.title, description, self.date, self.link, self.source, datetime.strptime(self.date, '%m/%d/%Y').date().isocalendar()[1] ]
