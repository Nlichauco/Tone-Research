from entity.ToneStat import ToneStat


class Week:
    """Week class which holds all tone data from a singular week.

    Week class has all tone data for that week.

  Attributes:
      weekname: weekname is there to be able to identiy different weeks.
      List_Arts: A list of article class objects.
     """

    def __init__(self, week_name):
        self.weekname = week_name
        self.List_Arts = list()
        self.Sadness = ToneStat("Sadness")
        self.Anger = ToneStat("Anger")
        self.Tenta = ToneStat("Tenta")
        self.Joy = ToneStat("Joy")
        self.Analy = ToneStat("Analy")
        self.Confi = ToneStat("Confi")
        self.Fear = ToneStat("Fear")

    def add_Art(self, art):
        # Add an article to the week, this function updates all scores for the week with the incoming articles data.
        self.List_Arts.append(art)
        self.Analy.add_score(art.analytical)
        self.Sadness.add_score(art.sadness)
        self.Confi.add_score(art.confidence)
        self.Anger.add_score(art.anger)
        self.Tenta.add_score(art.tentative)
        self.Fear.add_score(art.fear)
        self.Joy.add_score(art.joy)
