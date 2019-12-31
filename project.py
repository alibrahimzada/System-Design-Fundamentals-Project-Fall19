# importing necessary modules for project
import board
import digitalio
import time
import adafruit_hcsr04
import pulseio


#Reading drivers for hardwares and introducing them to computer
buzzer = pulseio.PWMOut(board.D8, variable_frequency=True)
sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.D10, echo_pin=board.D9)
red_led = digitalio.DigitalInOut(board.D3)
yellow_led= digitalio.DigitalInOut(board.D2)
green_led = digitalio.DigitalInOut(board.D1)
red_led.direction = digitalio.Direction.OUTPUT
yellow_led.direction = digitalio.Direction.OUTPUT
green_led.direction = digitalio.Direction.OUTPUT


class SM:
    """
    The State Machine class implements State Machine operations.
    Attributes:
        None
    Methods:
        start(self): The method to start the SM and set the start state.
        step(self, inp): The method to handle output and set new state at each step.
        transduce(self, input): The method that gets new inputs and give it for self.step.
    """

    def start(self):
        """
        The method to start the SM and set the start state.
        Parameters:
            None
        Returns:
            None
        """

        self.state = self.startState

    def step(self, inp):
        """
        The method to handle output and set new state at each step.
        Parameters:
            inp (float): input value given to state machine at each step
        Returns:
            o (str): output value from a certain state
        """

        (s, o) = self.getNextValues(self.state, inp)

        if s != 'closedState':
            self.state = s
            self.isFinalState = False
            self.start = 0
        elif s == 'closedState' and not self.isFinalState:
            self.start = time.time()
            self.isFinalState = True
        elif s == 'closedState' and self.getTimeDiffernce(self.start) > 5:
            self.state = 'finalState'
        return o

    def transduce(self, input):
        """
        The method that gets new inputs and give it for self.step.
        Parameters:
            input (float): The input value given to state machine at each step from sonars.
        Returns:
            self.state (str): new state of state machine.
            o (str): output value from a certain state
        """

        if not self.checkState:
            self.start()
            self.checkState = True
        o = self.step(input)
        return (self.state, o)

    def getTimeDiffernce(self, old_time):
        return time.time() - old_time


class ObstacleDetector(SM):
    """
    The ObstacleDetector class which implements the states of project.
    Attributes:
        startState (str): start state of the state machine.
        checkState (bool): check state in certain points.
    Methods:
        initialize(self, led): The method which encapsulates a specific functionaility.
        getNextValues(self, state, inp): The method which handles states based on inputs and current state.
    """

    startState = 'initialState'
    checkState = False
    isFinalState = False
	
    def initialize(self, led):
        """
        The method which encapsulates a specific functionaility.
        Parameters:
            led (instance): LEDs from circuit

        Returns:
            None
        """

        led.value = True
        time.sleep(2)
        led.value = False
        time.sleep(1)

    def getNextValues(self, state, inp):
        """
        The method which handles states based on inputs and current state.
        Parameters:
            state (str): The current state of state machine.
            inp (float): The input value for state machine from sonars.

        Returns:
            nextState (str): Next state based on the input value.
            output (str): Output value based on the input value.
        """

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
            buzzer.duty_cycle = 0
            return ('fourthState', 'DANGER TOO CLOSE')

        elif inp >= 200:
            red_led.value = False
            green_led.value = True
            yellow_led.value = True
            buzzer.duty_cycle = 0
            return ('fifthState', 'Distance Error')

        elif inp <= 25:
            return ('closedState', '')


def getTimeDifference(old_time):
    """
    The function which calculates time difference.
    Parameters:
        old_time (float): The old time in which the interval started.
    Returns:
        difference (float): The time difference between old_time and current time.
    """

    return time.time() - old_time


obj = ObstacleDetector()                                 # An ObstacleDetector instance to start the project
while True:                                    # An infinite loop to test the Obstacle Detector in real time
    try:
        sonar_distance = sonar.distance
    except RuntimeError:                     # Catching RuntimeError when waves cannot return back to sensor
        sonar_distance = 200
    (s, o) = obj.transduce(sonar_distance)       # New state and output based on the given input from sonars
    print(sonar_distance, s, o)                                          # Displaying the output on terminal

    if s == 'finalState':                                              # Checking if the SM is in finalState
        print('The Device Stopped! Calling Emergency Services')   # final output before stopping the program
        green_led.value = False
        yellow_led.value = False
        red_led.value = True
        buzzer.duty_cycle = 2**15
        time.sleep(1)
        break