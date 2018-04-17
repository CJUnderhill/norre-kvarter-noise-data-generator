import csv
import random

COMM_STREETS = {'Sankt Peters Straede': (29, 53),
                'Studiestraede': (6, 49),
                'Vestergade': (1, 26),
                'Norregade': (23, 53),
                'Teglgardstraede': (2, 17),
                'Larsbjornstraede': (2, 25)}

RES_STREETS = {'Norre Voldgade': (2, 60),
               'Sankt Peters Strade': (1, 53),
               'Studiestraede': (1, 49),
               'Gammeltorv': (8, 18),
               'Vestergade': (1, 39),
               'Norregade': (2, 53),
               'Larslejsstraede': (1, 19),
               'Teglgardstraede': (2, 17),
               'Larsbjornstraede': (2, 25),
               'Vester Volgade': (2, 37)}


class Complaint:

    def __init__(self):
        self.weekend = False
        self.category = None
        self.sub_category = None
        self.time = None
        self.location = None

    def __iter__(self):
        return iter([self.weekend, self.category, self.sub_category, self.time, self.location])

    def getWeekend(self):
        return self.weekend

    def setWeekend(self, status):
        self.weekend = status

    def getCategory(self):
        return self.category

    def setCategory(self, status):
        self.category = status

    def getSubCategory(self):
        return self.sub_category

    def setSubCategory(self, status):
        self.sub_category = status

    def getTime(self):
        return self.time

    def setTime(self, status):
        self.time = status

    def getLocation(self):
        return self.location

    def setLocation(self, status):
        self.location = status


def main(iterations):
    complaint_list = []

    for x in range(0, iterations):
        random.seed(None)
        complaint = Complaint()

        complaint.setWeekend(isWeekend())
        complaint.setCategory(chooseCategory(complaint.getWeekend()))
        complaint.setSubCategory(chooseSubCategory(complaint.getCategory()))
        complaint.setTime(chooseTime(complaint.getWeekend(), complaint.getCategory()))
        complaint.setLocation(chooseLocation(complaint.getCategory()))
        complaint_list.append(complaint)

    with open('test.csv', 'w', newline='') as csv_file:
        wr = csv.writer(csv_file, delimiter=',')
        wr.writerow(['Weekend?', 'Category', 'Sub Category', 'Time', 'Location'])
        for c in complaint_list:
            wr.writerow(c)


def isWeekend():
    p = random.random()
    return True if p < .8 else False


def chooseCategory(isWeekend):
    category = None
    p = random.random()

    if isWeekend:
        if p < .35:
            category = "Bar"
        elif p < .5:
            category = "Construction"
        elif p < .9:
            category = "Street"
        else:
            category = "Private"
    else:
        if p < .25:
            category = "Bar"
        elif p < .6:
            category = "Construction"
        elif p < .9:
            category = "Street"
        else:
            category = "Private"

    return category


def chooseSubCategory(category):
    sub_category = None
    p = random.random()

    if category == "Bar":
        if p < .4:
            sub_category = "Music/General Noise"
        elif p < 1:
            sub_category = "Talking"
        else:
            sub_category = "Banging"
    elif category == "Construction":
        if p < .5:
            sub_category = "Music/General Noise"
        elif p < .5:
            sub_category = "Talking"
        else:
            sub_category = "Banging"
    elif category == "Street":
        if p < .4:
            sub_category = "Music/General Noise"
        elif p < .9:
            sub_category = "Talking"
        else:
            sub_category = "Banging"
    else:
        if p < .7:
            sub_category = "Music/General Noise"
        elif p < .9:
            sub_category = "Talking"
        else:
            sub_category = "Banging"

    return sub_category


def chooseTime(isWeekend, category):
    import time as timeModule
    from datetime import datetime, timedelta

    start = timeModule.mktime(timeModule.strptime("8 Mar 18", "%d %b %y"))
    end = timeModule.time()

    newtime = random.randint(int(start), int(end))
    newdatetime = datetime.fromtimestamp(newtime)

    hour = None

    if isWeekend:
        while True:
            if newdatetime.weekday() == 4 or newdatetime.weekday() == 5 or newdatetime.weekday() == 6:
                break
            else:
                newdatetime = datetime.fromtimestamp(random.randint(int(start), int(end)))
    else:
        while True:
            if newdatetime.weekday() == 4 or newdatetime.weekday() == 5 or newdatetime.weekday() == 6:
                newdatetime = datetime.fromtimestamp(random.randint(int(start), int(end)))
            else:
                break

    # print(newtime)
    # print(newdatetime)

    p = random.random() * 2
    time = None

    weekend_factor_day = 0
    weekend_factor_night = 0
    weekend_factor_peak = 0
    weekend_factor_close = 0

    category_factor_day = 0
    category_factor_night = 0
    category_factor_peak = 0
    category_factor_close = 0

    if isWeekend:
        weekend_factor_day = .05
        weekend_factor_night = .4
        weekend_factor_peak = .5
        weekend_factor_close = .05
    else:
        weekend_factor_day = .15
        weekend_factor_night = .15
        weekend_factor_peak = .35
        weekend_factor_close = .35

    if category == "Bar":
        category_factor_day = 0
        category_factor_night = .15
        category_factor_peak = .5
        category_factor_close = .35
    elif category == "Construction":
        category_factor_day = .8
        category_factor_night = .2
        category_factor_peak = 0
        category_factor_close = 0
    elif category == "Street":
        category_factor_day = .05
        category_factor_night = .1
        category_factor_peak = .35
        category_factor_close = .5
    else:
        category_factor_day = 0
        category_factor_night = .35
        category_factor_peak = .65
        category_factor_close = 0

    factor_day = weekend_factor_day + category_factor_day
    factor_night = weekend_factor_night + category_factor_night
    factor_peak = weekend_factor_peak + category_factor_peak
    factor_close = weekend_factor_close + category_factor_close

    if p < factor_day:
        time = "Day"
    elif p < factor_day + factor_night:
        time = "Night"
    elif p < factor_day + factor_night + factor_peak:
        time = "Peak"
    else:
        time = "Close"

    if time == "Day":
        hour = random.randrange(8, 18)
    elif time == "Night":
        hour = random.randrange(18, 22)
    elif time == "Peak":
        hour = random.randrange(22, 26)
        if hour > 23:
            hour = hour - 23
            newdatetime += timedelta(days=1)
    else:
        hour = random.randrange(2, 6)
        newdatetime += timedelta(days=1)

    newdatetime = newdatetime.replace(hour=hour, minute=random.randrange(0, 59), second=random.randrange(0, 59))

    # print(newdatetime)

    return newdatetime


def chooseLocation(category):
    p = random.random()
    location = None
    address_range = None

    if category == "Bar" or category == "Street":
        if p < .17:
            location = "Sankt Peters Straede"
        elif p < .34:
            location = "Studiestraede"
        elif p < .51:
            location = "Vestergade"
        elif p < .68:
            location = "Norregade"
        elif p < .85:
            location = "Teglgardstraede"
        else:
            location = "Larsbjornstraede"

        address_range = COMM_STREETS[location]

    else:
        if p < .11:
            if p < .05:
                location = "Gammeltorv"
            else:
                location = "Larslejsstraede"
        elif p < .22:
            location = "Norre Voldgade"
        elif p < .33:
            location = "Sankt Peters Strade"
        elif p < .44:
            location = "Studiestraede"
        elif p < .55:
            location = "Vestergade"
        elif p < .66:
            location = "Norregade"
        elif p < .77:
            location = "Teglgardstraede"
        elif p < .88:
            location = "Larsbjornstraede"
        else:
            location = "Vester Volgade"

        address_range = RES_STREETS[location]

    # Query Street dict and choose random address number
    address = random.randint(address_range[0], address_range[1])

    full_address = location + " " + str(address) + ", Copenhagen, Denmark"

    # geolocator = Nominatim()

    # geolocation = geolocator.geocode(full_address + ", Kødbyen, Vesterbro, København, Københavns Kommune, Region Hovedstaden, 1358, Danmark")
    # geolocation = geolocator.reverse("55.6799259, 12.5674304")

    # print(geolocation.address)
    # print((geolocation.latitude, geolocation.longitude))

    return full_address


# -------------------------------
if __name__ == "__main__":
    main(8500)
