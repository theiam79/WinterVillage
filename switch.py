from pybricks.hubs import CityHub
from pybricks.pupdevices import Motor, ColorDistanceSensor
from pybricks.parameters import Port, Color
from pybricks.tools import wait, StopWatch, multitask, run_task
from communications import SWITCH_CHANNEL, THROW, RESET
# from enum import Enum

# class ThrowDirection(Enum):
#     OPEN = -1
#     CLOSE = 1

# STARTING_DIRECTION = ThrowDirection.CLOSE
THROW_SPEED = 360
INITIAL_STATE = 1

current_state = INITIAL_STATE

hub = CityHub(observe_channels=[SWITCH_CHANNEL])

switchA_motor = Motor(Port.A)

async def setInitialState():
    global current_state
    await throwSwitch(INITIAL_STATE)
    current_state = INITIAL_STATE

async def throwSwitch(targetState):
    global current_state
    await switchA_motor.run_until_stalled(THROW_SPEED * targetState)

async def main():
    global current_state
    await setInitialState()
    data = 0
    lastSwitched = StopWatch()
    while True:
        data = hub.ble.observe(SWITCH_CHANNEL)
        if data is not None:
            if data != current_state:
                await throwSwitch(data)
                current_state = data
            # if data == THROW:
            #     newState = current_state * -1
            #     await throwSwitch(newState)
            #     current_state = newState
            # elif data == RESET:
            #     await setInitialState()
        await wait(10)

run_task(main())

