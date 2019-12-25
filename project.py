from SM import SM
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

class ObstacleDetector(SM):
    startState = 'nothing'

    def getNextValues(self, state, inp):

        # First State Discuss with group Members

        if inp > 120 and inp < 200: #Second State
            print("You are Safe")
            green_led.value = True
            red_led.value = False
            yellow_led.value = False
        elif inp <= 120 and inp > 50: #Third State
            print("Slow Down Your Speed")
            yellow_led.value = True
            green_led.value = False
            red_led.value = False
        elif inp <= 50 and inp > 25:    #Fourth State
            print("DANGER TOO CLOSE")
            red_led.value = True
            green_led.value = False
            yellow_led.value = False
        elif inp >= 200: #Discuss with group members Fifth State
            pass
        elif inp <= 25: #Discuss with group memebers Sixth State
            red_led.value = True
            green_led.value = False
            yellow_led.value = False




CarSensor = ObstacleDetector()
while True:	#Discuss State and while loop with group memebers
    CarSensor.getNextValues(0, sonar.distance)