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
                    
        elif 120 < inp < 200:                   #Second State
            green_led.value = True
            return ('thirdState', 'You are safe')
        
#        if inp > 120 and inp < 200: #Second State
#            print("You are Safe")
#            green_led.value = True
#            red_led.value = False
#            yellow_led.value = False
#        elif inp <= 120 and inp > 50: #Third State
#            print("Slow Down Your Speed")
#            yellow_led.value = True
#            green_led.value = False
#            red_led.value = False
#        elif inp <= 50 and inp > 25:    #Fourth State
#            print("DANGER TOO CLOSE")
#            red_led.value = True
 #           green_led.value = False
  #          yellow_led.value = False
   #     elif inp >= 200: #Discuss with group members Fifth State
    #        pass
     #   elif inp <= 25: #Discuss with group memebers Sixth State
      #      red_led.value = True
       #     green_led.value = False
        #    yellow_led.value = False




CarSensor = ObstacleDetector()
(s, o) = CarSensor.transduce(sonar.distance)
print(s, o)

while True:	#Discuss State and while loop with group memebers
    (s, o) = CarSensor.getNextValues(s, sonar.distance)
    print(sonar.distance)
    print(s, o)