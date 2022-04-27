import random
import datetime


def today_quote():
    with open("quotes.txt") as file:
        list_quotes = file.readlines()

    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    current_day = weekdays[datetime.datetime.now().weekday()]
    current_quote = random.choice(list_quotes)
    return [current_day, current_quote]
