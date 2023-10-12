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
    TURN_ON = ("1", )
    TURN_OFF = ("2", )


# ,--------------------------------.
# | oooooooooooooooooooo J8     +====
# | 1ooooooooooooooooooo        | USB
# |                             +====
# |      Pi Model 3B  V1.2         |
# |      +----+                 +====
# | |D|  |SoC |                 | USB
# | |S|  |    |                 +====
# | |I|  +----+                    |
# |                   |C|     +======
# |                   |S|     |   Net
# | pwr        |HDMI| |I||A|  +======
# `-| |--------|    |----|V|-------'
# 
# J8:
#    3V3  (1) (2)  5V      (1)-> Relayboard VCC, (2)-> Relayboard JD-VCC
#  GPIO2  (3) (4)  5V    
#  GPIO3  (5) (6)  GND   
#  GPIO4  (7) (8)  GPIO14  (7)-> PUMP_1, (8)-> VENT_1
#    GND  (9) (10) GPIO15
# GPIO17 (11) (12) GPIO18
# GPIO27 (13) (14) GND   
# GPIO22 (15) (16) GPIO23
#    3V3 (17) (18) GPIO24
# GPIO10 (19) (20) GND   
#  GPIO9 (21) (22) GPIO25
# GPIO11 (23) (24) GPIO8 
#    GND (25) (26) GPIO7 
#  GPIO0 (27) (28) GPIO1 
#  GPIO5 (29) (30) GND   
#  GPIO6 (31) (32) GPIO12
# GPIO13 (33) (34) GND   
# GPIO19 (35) (36) GPIO16
# GPIO26 (37) (38) GPIO20
#    GND (39) (40) GPIO21  (40)-> Relayboard Ground

class Device(AbstractEnum):
    """ Device = (Configcode, GPIO_PIN) for mode = GPIO.BOARD """
    PUMP_1 = ("P1", 7)
    VENT_1 = ("V1", 8)


class State(AbstractEnum):
    TURNED_ON = ("ON", )
    TURNED_OFF = ("OFF", )


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


# initialisation
GPIO.setmode(GPIO.BOARD)
GPIO.setup(Device.PUMP_1.value[1], GPIO.OUT)
# High voltage means that the relay is not switched on
GPIO.output(Device.PUMP_1.value[1], GPIO.HIGH)
GPIO.setup(Device.VENT_1.value[1], GPIO.OUT)
GPIO.output(Device.VENT_1.value[1], GPIO.HIGH)


if __name__ == '__main__':

    for i in range(3):
        GPIO.output(7, GPIO.LOW)
        time.sleep(0.5)
        
        GPIO.output(7, GPIO.HIGH)
        time.sleep(0.5)
