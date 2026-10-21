from datetime import timedelta

SUBSTITUI = ["proximo_dia_util"]


def proximo_dia_util(data):
    while data.weekday() > 5:
        data += timedelta(days=1)
    return data
