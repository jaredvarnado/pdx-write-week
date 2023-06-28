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
