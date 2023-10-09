import enum
import json
import datetime as dt
import time

from typing import NamedTuple, Dict


class AbstractEnum(enum.Enum):
    @classmethod
    def get_from_code(cls, entry_id: str):
        for enum_entry in cls:
            if entry_id == enum_entry.value:
                return enum_entry


class Action(AbstractEnum):
    TURN_ON = "1"
    TURN_OFF = "2"


class Device(AbstractEnum):
    PUMP_1 = "P1"
    VENT_1 = "V1"


class State(AbstractEnum):
    TURNED_ON = "ON"
    TURNED_OFF = "OFF"


class Event(NamedTuple):
    start_time: dt.time
    end_time: dt.time | None
    device: Device
    action: Action


class DeviceState:
    def __init__(self, device: Device, state: State):
        self.device = device
        self.state = state


def time_in_range(start: time, end: time, x: time) -> bool:
    """Return true if x is in the range [start, end]"""
    if start <= end:
        return start <= x <= end
    else:  # end is on the next day
        return start <= x or x <= end


def turn_on_device(device: Device, device_states: Dict[Device, DeviceState]):
    """Turn on the specified device"""
    None


def turn_off_device(device: Device, device_states: Dict[Device, DeviceState]):
    """Turn off the specified device"""
    None



# load the schedules
with open("schedules.json", "r") as f:
    schedules = json.load(f)

# init
device_states = {
    Device.PUMP_1: DeviceState(device=Device.PUMP_1, state=State.TURNED_OFF),
    Device.VENT_1: DeviceState(device=Device.VENT_1, state=State.TURNED_OFF),
}

events = []

# build eventlist from configured schedules, ordered by time
# why? in order to know how long the process can sleep till the next event
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

print(events)


while True:
    now = dt.datetime.now().time()
    for event in events:
        if event.action == Action.TURN_ON:
            if time_in_range(event.start_time, event.end_time, now):
                if device_states.get(event.device).state == State.TURNED_OFF:
                    turn_on_device(event.device, device_states)
            elif device_states.get(event.device).state == State.TURNED_ON:
                turn_off_device(event.device, device_states)
        # ToDo: get the time till the next event and set the process to sleep accordingly

    time.sleep(2)


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


if __name__ == '__main__':
    print_hi('there')

