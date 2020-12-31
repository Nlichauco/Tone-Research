from datetime import timedelta, date


def get_date_nyt_format(q, start, end):
    def date_range(date1, date2):
        add = 1 if q == 6 else 0
        for n in range(q, int((date2 - date1).days) + add, 7):
            yield date1 + timedelta(n)

    end_date = []
    for dt in date_range(start, end):
        end_date.append(dt.strftime("%m%d"))
    return end_date


"""Creates dates to easily go week by week for queries

    Args:
        for now none

    Returns:
         A list of dates."""


def get_date_guardian_format(q, start, end):
    def date_range(date1, date2):
        add = 1 if q == 6 else 0
        for n in range(q, int((date2 - date1).days) + add, 7):
            yield date1 + timedelta(n)

    end_date = []
    for dt in date_range(start, end):
        end_date.append(dt.strftime("%m-%d"))
    return end_date
