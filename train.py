from pybricks.hubs import CityHub
from pybricks.pupdevices import DCMotor, ColorDistanceSensor
from pybricks.parameters import Port, Color
from pybricks.tools import wait, StopWatch
from communications import SWITCH_CHANNEL, THROW, RESET

LAPS_PER_ROUTE = 2
TRAVEL_SPEED = 50
SLOWING_SPEED = 30
BOARDING_DELAY = 10 * 1000
INNER_LOOP_TIME = 10
MIN_LAP_TIME = 5 * 1000
MIN_COLOR_COUNT = 7
IGNORED_COLORS = [Color.BLUE]
STOP_DEBOUNCE_TIME = 5*1000

hub = CityHub(broadcast_channel=SWITCH_CHANNEL)

train_motor = DCMotor(Port.A)
color_sensor = ColorDistanceSensor(Port.B)

passengers_waiting = False
lap_count = 0
lap_timer = StopWatch()
last_stopped = StopWatch()

# train_motor.dc(50)

# wait(2000)

# train_motor.dc(0)
def main():
    print('Start Main')
    startRoute()
    print('Start Loop')
    #main loop
    loopCount = 0
    while True:
        wait(INNER_LOOP_TIME)
        # loopCount += 1
        # if loopCount >= 150:
        #     print('Resetting Broadcast')
        #     hub.ble.broadcast(None)
        #     loopCount = 0
        color = color_sensor.color()
        handleColor(color)

current_color = Color.MAGENTA
color_count = 0

def handleColor(color):
    global current_color
    global color_count
    global last_stopped
    # print(f'Current: {current_color} x {color_count} => {color}')

    if color in IGNORED_COLORS:
        return

    if current_color != color:
        current_color = color
        color_count = 0
    elif color_count >= MIN_COLOR_COUNT:
        print(f'Found {color} {color_count} time(s), resetting')
        color_count = 0
        if color == Color.YELLOW:
            slowTrain()
        elif color == Color.RED and last_stopped.time() >= STOP_DEBOUNCE_TIME:
            stopAndWaitForPassengers()
        elif color == Color.GREEN:
            countLap()
        else:
            print('No Action Taken')
    else:
        color_count += 1

def countLap():
    global lap_count
    global passengers_waiting
    global lap_timer
    print(lap_timer.time())
    if(lap_timer.time() >= MIN_LAP_TIME):
        lap_timer.reset()
        lap_count += 1
        print(f'Finished lap {lap_count}/{LAPS_PER_ROUTE}')
        passengers_waiting = lap_count >= LAPS_PER_ROUTE
        if passengers_waiting:
            print("Throwing switch")
            hub.ble.broadcast(THROW)
            print("Route complete, stopping next lap")

def startRoute():
    global lap_timer
    global last_stopped
    print('Start route')
    train_motor.dc(TRAVEL_SPEED)
    print('Resetting switch')
    hub.ble.broadcast(RESET)
    lap_timer.resume()
    last_stopped.reset()

def slowTrain():
    global passengers_waiting
    if (passengers_waiting):
        print('Begin Slowing')
        train_motor.dc(SLOWING_SPEED)

def stopAndWaitForPassengers():
    global lap_count
    global passengers_waiting
    global lap_timer
    print('Stopping for passengers')
    train_motor.dc(0)
    lap_timer.pause()
    wait(BOARDING_DELAY)
    lap_count = 0
    passengers_waiting = False
    startRoute()

main()