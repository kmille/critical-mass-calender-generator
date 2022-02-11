import calendar
import json
import arrow
from ics import Calendar, Event
from ics.alarm import DisplayAlarm

#json_file = "cm.json"
json_file = "cities.json"
ical_name = "cm.ics"

days = {'Montag': calendar.MONDAY,
        'Dienstag': calendar.TUESDAY,
        'Mittwoch': calendar.WEDNESDAY,
        'Donnerstag': calendar.THURSDAY,
        'Freitag': calendar.FRIDAY,
        'Samstag': calendar.SATURDAY,
        'Sonntag': calendar.SUNDAY,
        'Monday': calendar.MONDAY,
        'Tuesday': calendar.TUESDAY,
        'Wednesday': calendar.WEDNESDAY,
        'Thursday': calendar.THURSDAY,
        'Friday': calendar.FRIDAY,
        'Saturday': calendar.SATURDAY,
        'Sunday': calendar.SUNDAY,
        }


def get_event(name, infos, cal=None):
    c = Calendar() if not cal else cal
    year = arrow.now().year
    for month in range(arrow.now().month, 13):
        day = days[infos['day']]
        all_days_per_month = [week[day]
                              for week in calendar.monthcalendar(year, month)]
        if all_days_per_month[0] == 0:
            all_days_per_month.pop(0)
        selected_day = all_days_per_month[infos['cycle']]
        begin_str = '{:4d}-{:02d}-{:02d} {}:00 Europe/Berlin'.format(
            year, month, selected_day, infos['begin'])
        begin = arrow.get(begin_str, 'YYYY-MM-DD HH:mm:ss ZZZ')
        end = begin.replace(hour=begin.hour+2)
        alarm = DisplayAlarm(display_text='Endlich wieder ' + name,
                             trigger=begin.shift(days=-4))
        e = Event()
        e.name = "Critical Mass " + name
        e.location = infos['location']
        e.begin = begin
        e.end = end
        e.description = infos.get('url', "")
        e.alarms = (alarm, )
        c.events.add(e)
    print("Done with {}".format(name))
    return c


events = json.load(open(json_file, "r"))
cal = Calendar()
for name, infos in events.items():
    # if name in ("Würzburg", "Darmstadt"):
    if name in ("Darmstadt"):
        get_event(name, infos, cal)
#[get_event(event, cal) for event in events]

with open(ical_name, "w") as f:
    f.writelines(cal)
