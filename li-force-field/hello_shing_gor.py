#!/usr/bin/env python3

"""
Li's force field confirmator
"""

import datetime

MONTH_TO_NUMBER = { month: idx + 1 for idx, month in enumerate(["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]) }

HOURS_PER_SEGMENT = 2  # must be factor of 24 i.e. 1,2,4,6,8,etc.

def read_holidays():
    data = {}
    with open("holidays.txt") as fp:
        lines = fp.read().split("\n")
        current = None
        for line in lines:
            if line.strip() == "":
                continue

            if line.find("\t") == -1:
                year = int(line)
                current = year
                data[year] = []
                continue

            if line.find("Every Sunday") != -1:
                continue

            name, day, dow = line.split("\t")

            dom, month = day.split()
            dom = int(dom)
            data[year].append((MONTH_TO_NUMBER[month[:3].lower()], dom))

    return data

HOLIDAYS = read_holidays()

def is_holiday(yyyy, mm, dd):
    if datetime.datetime(yyyy, mm, dd).isoweekday() in (6, 7):
        return True

    if yyyy not in HOLIDAYS:
        return None # no vs dunno

    return (mm, dd) in HOLIDAYS[yyyy]

def is_friday(yyyy, mm, dd):
    return datetime.datetime(yyyy, mm, dd).isoweekday() == 5

def read_typhoon():
    data = []
    with open("typhoon.txt") as fp:
        lines = fp.read().split("\n")
        for line in lines:
            if line.strip() == "":
                continue

            if line.startswith("#"):
                continue

            # print(line.split("\t"))
            intensity, name, signal, start_time, start_date, end_time, end_date, duration = line.split("\t")

            data.append((signal, start_time, start_date, end_time, end_date, signal not in ('1', '3')))

    return data

def read_rainstorm():
    data = []
    with open("rainstorm.txt") as fp:
        lines = fp.read().split("\n")
        for line in lines:
            if line.strip() == "":
                continue

            if line.startswith("#"):
                continue

            # print(line.split("\t"))
            color, start_time, start_date, end_time, end_date, duration = line.split("\t")

            data.append((color, start_time, start_date, end_time, end_date, color == 'Black'))

    return data

class Event:
    def __init__(self, originally_need_work, cant_work, time_segment):
        self.cant_work = cant_work
        self.originally_need_work = originally_need_work
        self.time_segment = time_segment

    def tuple(self):
        return (self.originally_need_work, self.cant_work, self.time_segment)

def chartable_info(reader, select_datetime):
    data = []

    for xx, start_time, start_date, end_time, end_date, cant_work in reader():
        dd, emonth, yyyy = select_datetime({"start":start_date, "end":end_date}).split("/")
        dd = int(dd)
        yyyy = int(yyyy)
        mm = MONTH_TO_NUMBER[emonth[:3].lower()]
        hour = int(select_datetime({"start":start_time, "end":end_time}).split(":")[0]) // HOURS_PER_SEGMENT

        data.append(Event(bool(is_holiday(yyyy, mm, dd)), cant_work, hour).tuple())

    return data

def aggregate_data(reader, select_datetime):
    import collections
    aggregate = collections.Counter()

    for entry in chartable_info(reader, select_datetime):
        aggregate[entry] += 1

    return aggregate


if __name__ == "__main__":
    print("Need work")
    select_holiday = False

    # program parameters here:
    agg = aggregate_data(read_typhoon, lambda d: d["start"])

    for segment in range(0, 24//HOURS_PER_SEGMENT):
        print("%02dh-%02dh" % (segment * HOURS_PER_SEGMENT, (segment+ 1) * HOURS_PER_SEGMENT), agg[(select_holiday, True, segment)], agg[(select_holiday, False, segment)])

    print("-------------")
    print("No need work")
    select_holiday = True
    for segment in range(0, 24//HOURS_PER_SEGMENT):
        print("%02dh-%02dh" % (segment * HOURS_PER_SEGMENT, (segment+ 1) * HOURS_PER_SEGMENT), agg[(select_holiday, True, segment)], agg[(select_holiday, False, segment)])
