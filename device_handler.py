import enum
import RPi.GPIO as GPIO
import time


class AbstractEnum(enum.Enum):
    @classmethod
    def get_from_code(cls, entry_code: str):
        for enum_entry in cls:
            if entry_code == enum_entry.value[0]:
                return enum_entry


class Action(AbstractEnum):
    TURN_ON = ("1",)
    TURN_OFF = ("2",)


class Device(AbstractEnum):
    """ Device = (Configcode, GPIO_PIN) for mode = GPIO.BOARD
        see README file for pin assignment
    """
    PUMP_1 = ("P1", 7)
    VENT_1 = ("V1", 8)


class State(AbstractEnum):
    TURNED_ON = ("ON",)
    TURNED_OFF = ("OFF",)


class DeviceState:
    def __init__(self, device: Device, state: State):
        self.device = device
        self.state = state


def turn_on_device(device_state: DeviceState):
    """Turn on the specified device"""
    # Low voltage means that the relay is switched on
    GPIO.output(device_state.device.value[1], GPIO.LOW)
    device_state.state = State.TURNED_ON


def turn_off_device(device_state: DeviceState):
    """Turn off the specified device"""
    # High voltage means that the relay is not switched on
    GPIO.output(device_state.device.value[1], GPIO.HIGH)
    device_state.state = State.TURNED_OFF


# init
device_states = {
    Device.PUMP_1: DeviceState(device=Device.PUMP_1, state=State.TURNED_OFF),
    Device.VENT_1: DeviceState(device=Device.VENT_1, state=State.TURNED_OFF),
}

# initialisation
GPIO.setmode(GPIO.BOARD)
GPIO.setup(Device.PUMP_1.value[1], GPIO.OUT)
# High voltage means that the relay is not switched on
GPIO.output(Device.PUMP_1.value[1], GPIO.HIGH)
GPIO.setup(Device.VENT_1.value[1], GPIO.OUT)
GPIO.output(Device.VENT_1.value[1], GPIO.HIGH)

if __name__ == '__main__':
    # Set low voltage to switch the relay to NO (Normally Open) = Turn on
    GPIO.output(Device.VENT_1, GPIO.LOW)
    GPIO.output(Device.PUMP_1, GPIO.LOW)
    time.sleep(10)

    GPIO.output(Device.VENT_1, GPIO.HIGH)
    GPIO.output(Device.PUMP_1, GPIO.HIGH)
    time.sleep(10)
