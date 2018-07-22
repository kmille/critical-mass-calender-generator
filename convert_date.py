import calendar
import json
import arrow
from ics import Calendar, Event
from ics.alarm import DisplayAlarm
from ipdb import set_trace

json_file = "cm.json"
ical_name = "cm.ics"

days = { 'Montag':     calendar.MONDAY,
         'Dienstag':   calendar.TUESDAY,
         'Mittwoch':   calendar.WEDNESDAY,
         'Donnerstag': calendar.THURSDAY,
         'Freitag':    calendar.FRIDAY,
         'Samstag':    calendar.SATURDAY,
         'Sonntag':    calendar.SUNDAY,
         'Monday':     calendar.MONDAY,
         'Tuesday':    calendar.TUESDAY,
         'Wednesday':  calendar.WEDNESDAY,
         'Thursday':   calendar.THURSDAY,
         'Friday':     calendar.FRIDAY,
         'Saturday':   calendar.SATURDAY,
         'Sunday':     calendar.SUNDAY,
}
 
def get_event(mass, cal=None):
    c = Calendar() if not cal else cal
    year = arrow.now().year
    #for month in range(1, 13):
    for month in range(1, 13)[7:8]:
        day = days[mass['day']]
        all_days_per_month = [week[day] for week in calendar.monthcalendar(year, month)]
        selected_day = all_days_per_month[mass['cycle']]
        begin_str = '{:4d}-{:02d}-{:02d} {}:00'.format(year, month, selected_day, mass['begin'])
        begin = arrow.get(begin_str, 'YYYY-MM-DD HH:mm:ss')
        end = begin.replace(hour=begin.hour+2)
        alarm = DisplayAlarm(description='Endlich wieder ' + mass['name'], 
                             trigger=begin.replace(day=begin.day-4))
        e = Event()
        e.name = mass['name'] 
        e.location = mass['location']
        e.begin = begin
        e.end = end
        e.description = "\n".join(mass['urls'])
        e.alarms = (alarm, )
        c.events.add(e)
    return c

events = json.load(open(json_file, "r"))
cal = Calendar()
__ = [get_event(event, cal) for event in events]

with open(ical_name, "w") as f:
    f.writelines(cal)
