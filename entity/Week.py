from entity.ToneStat import toneStat


class Week:
    """Week class which holds all tone data from a singular week.

    Week class has all tone data for that week.

  Attributes:
      weekname: weekname is there to be able to identiy different weeks.
      List_Arts: A list of article class objects.
     """

    def __init__(self, week_name):
        self.weekname=week_name
        self.List_Arts=list()
        self.Sadness=toneStat("Sadness")
        self.Anger=toneStat("Anger")
        self.Tenta=toneStat("Tenta")
        self.Joy=toneStat("Joy")
        self.Analy=toneStat("Analy")
        self.Confi=toneStat("Confi")
        self.Fear=toneStat("Fear")

    def add_Art(self, art):
        #Add an article to the week, this function updates all scores for the week with the incoming articles data.
        self.List_Arts.append(art)
        self.Analy.add_score(art.analytical)
        self.Sadness.add_score(art.sadness)
        self.Confi.add_score(art.confidence)
        self.Anger.add_score(art.anger)
        self.Tenta.add_score(art.tentative)
        self.Fear.add_score(art.fear)
        self.Joy.add_score(art.joy)