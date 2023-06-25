class Event:
    def __init__(self, title, date, startTime, endTime, link):
        self.title = title
        self.date = date
        self.startTime = startTime
        self.endTime = endTime
        self.link = link

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
    def toString(self):
        return f"{self.title},{self.date},{self.startTime},{self.endTime},{self.link}"
