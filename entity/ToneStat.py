import statistics as stat


class ToneStat:
    """toneStat class which can grab median, max and avg from a weeks dataset.

    The toneStat class is inside the weeks class, it is used to get stats about the week.

    Attributes:
        Tone: Each toneStat class obj is responsible for one tone, the 'Tone' attribute holds the label to keep track of tones.
        Tone_Scores: the array which holds all scores associated with the Tone.
    """

    def __init__(self, tone_name):
        self.Tone = tone_name
        self.Tone_scores = []

    def add_score(self, score):
        # add a tone score to the array
        self.Tone_scores.append(score)

    def get_mean(self):
        my_sum = 0
        count = 0
        for score in self.Tone_scores:
            if score > .5:
                my_sum += score
                count += 1
        if my_sum != 0:
            return my_sum / count
        else:
            return .5

    def get_median(self):
        return stat.median(self.Tone_scores)

    def get_max(self):
        return max(self.Tone_scores)

    def get_perc(self):
        total = len(self.Tone_scores)
        if total == 0:
            return 0
        else:
            my_sum = 0
            for num in self.Tone_scores:
                if num > .5:
                    my_sum += 1
            return my_sum / total

    def get_total(self):
        total = 0
        for score in self.Tone_scores:
            if score > .5:
                total += score
        if total == 0:
            return .5
        return total
