class RSSIMeasure(object):
    def __init__(self, rss1, rss2, rss3):
        self.rss1 = rss1
        self.rss2 = rss2
        self.rss3 = rss3


class TimedRSSIMeasure(RSSIMeasure):
    def __init__(self, rss1, rss2, rss3, time):
        super().__init__(rss1, rss2, rss3)
        self.time = time

    def to_rssi_measure(self):
        return RSSIMeasure(self.rss1, self.rss2, self.rss3)

    def __str__(self):
        return "({}, {}, {}, {})".format(self.rss1, self.rss2, self.rss3, self.time)

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
