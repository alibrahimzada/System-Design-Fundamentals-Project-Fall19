import board
import digitalio
import time
import adafruit_hcsr04
import pulseio

buzzer = pulseio.PWMOut(board.D8, variable_frequency=True)
sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.D5, echo_pin=board.D0)
red_led = digitalio.DigitalInOut(board.D1)
yellow_led= digitalio.DigitalInOut(board.D2)
green_led = digitalio.DigitalInOut(board.D3)
red_led.direction = digitalio.Direction.OUTPUT
yellow_led.direction = digitalio.Direction.OUTPUT
green_led.direction = digitalio.Direction.OUTPUT


class SM:
    def start(self):
        self.state = self.startState
    
    def step(self, inp):
        (s, o) = self.getNextValues(self.state, inp)
        self.state = s
        return o
    
    def transduce(self, input):
        self.start()
        o = self.step(input)
        return (self.state, o)


class ObstacleDetector(SM):
    startState = 'initialState'

    def initialize(self, led):
        led.value = True
        time.sleep(2)
        led.value = False
        time.sleep(1)

    def getNextValues(self, state, inp):
        if state == 'initialState':
            self.initialize(green_led)
            self.initialize(yellow_led)
            self.initialize(red_led)
            buzzer.duty_cycle = 2**15
            time.sleep(2)
            buzzer.duty_cycle = 0
            return (None, 'Obstacle Detector Device is Working!')
                    
        elif 120 < inp < 200:
            red_led.value = False
            yellow_led.value = False
            green_led.value = True
            return ('secondState', 'You are safe')

        elif 50 < inp <= 120:
            green_led.value = False
            red_led.value = False
            yellow_led.value = True
            return ('thirdState', 'Slow Down Your Speed')

        elif 25 < inp <= 50:
            yellow_led.value = False
            green_led.value = False
            red_led.value = True
            return ('fourthState', 'DANGER TOO CLOSE') 

        elif inp >= 200:
            red_led.value = False
            green_led.value = True
            yellow_led.value = True
            return ('fifthState', 'Distance Error')
        
        elif inp <= 25:
            green_led.value = False
            yellow_led.value = False
            red_led.value = True
            buzzer.duty_cycle = 2**15
            return ('finalState', 'The Device Stopped! Calling the emergency services')


def getTimeDifference(old_time):
    return time.time() - old_time

obj = ObstacleDetector()
(s, o) = obj.transduce(sonar.distance)
print(s, o)

isFinalState = False
while True:
    (s, o) = obj.transduce(sonar.distance)
    print(sonar.distance, s, o)
    
    if not isFinalState and s == 'finalState':
        start = time.time()
        isFinalState = True
    elif s != 'finalState':
        isFinalState = False

    difference = getTimeDifference(start)
    if s == 'finalState' and difference > 5:
        print(o)
        break
