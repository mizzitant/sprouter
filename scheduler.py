import json
import datetime as dt
import time

from typing import NamedTuple, Dict, Optional

from device_handler import Action, Device, DeviceState, State
from device_handler import turn_on_device, turn_off_device, device_states


class Event(NamedTuple):
    start_time: dt.time
    end_time: Optional[dt.time]  # dt.time | Any
    device: Device
    action: Action


def time_in_range(start: time, end: time, x: time) -> bool:
    """Return true if x is in the range [start, end]"""
    if start <= end:
        return start <= x <= end
    else:  # end is on the next day
        return start <= x or x <= end


def time_till_next_event(events: list[Event]):
    """calculate the time from now till the next closest event"""
    # max sleeping intervall is from now till next day
    end_of_day = dt.datetime.now().replace(
        hour=23, minute=59, second=59, microsecond=999999)
    next_sleep_interval = end_of_day - dt.datetime.now()

    for event in events:
        now = dt.datetime.now()
        event_time = dt.datetime.combine(dt.date.today(), event.start_time)
        time_diff = event_time - now
        if time_diff.total_seconds() > 0:
            if time_diff < next_sleep_interval:
                next_sleep_interval = time_diff
    return next_sleep_interval.total_seconds()


def build_eventlist_from_schedules(schedules) -> list[Event]:
    """build eventlist from configured schedules, ordered by time"""
    events: list[Event] = []
    for schedule in schedules['schedules']:
        start_time = dt.datetime.strptime(schedule['starttime'], '%H:%M:%S').time()
        dur = dt.datetime.strptime(schedule['duration'], '%H:%M:%S')
        td = dt.timedelta(hours=dur.hour, minutes=dur.minute, seconds=dur.second)
        end_time = dt.datetime.combine(dt.date.today(), start_time) + td

        events.append(Event(start_time=start_time,
                            end_time=end_time.time(),
                            device=Device.get_from_code(schedule["device"]),
                            action=Action.TURN_ON
                            )
                      )
        events.append(Event(start_time=end_time.time(),  # does not work if the endtime is on the next day
                            end_time=None,
                            device=Device.get_from_code(schedule["device"]),
                            action=Action.TURN_OFF
                            )
                      )
    events.sort(key=lambda e: e.start_time)
    return events


events: list[Event] = None
while True:
    # load the schedules
    with open("schedules.json", "r") as f:
        schedules = json.load(f)

    # build eventlist from configured schedules, ordered by time
    # why? in order to know how long the process can sleep till the next event
    events = build_eventlist_from_schedules(schedules)

    now = dt.datetime.now().time()
    for event in events:
        if event.action == Action.TURN_ON:  # TURN_ON has start and end time
            if time_in_range(event.start_time, event.end_time, now):
                if device_states.get(event.device).state == State.TURNED_OFF:
                    turn_on_device(device_states.get(event.device))
            else:  # outside of turned on timerange turn it off
                if device_states.get(event.device).state == State.TURNED_ON:
                    turn_off_device(device_states.get(event.device))

        # ToDo: get the time till the next event and set the process to sleep accordingly

    time.sleep(time_till_next_event(events))
    # ToDo: check if events actually where triggered


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


if __name__ == '__main__':
    print_hi('there')
