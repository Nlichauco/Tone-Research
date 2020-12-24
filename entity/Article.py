"""
Class Article
-Scores set to .5 by default
"""
class Article:
    def __init__(self, source, date,url):
        self.source=source
        self.published=date
        self.url=url
        self.analytical=.5
        self.sadness=.5
        self.confidence=.5
        self.anger=.5
        self.tentative=.5
        self.fear=.5
        self.joy=.5