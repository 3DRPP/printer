try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!  This is probably because you need "
          "superuser privileges.  You can achieve this by using 'sudo' to run "
          "your script")

gpios = [3, 5, 7, 8, 10, 11, 12, 13, 15, 16, 18, 19, 21, 22, 23, 24, 26, 29,
         31, 32, 33, 35, 36, 37, 38, 40]

class Pin:
    def __init__(self, number, value):
        self.number = number
        self.value = value

    def set_value(self, value):
        try:
            GPIO.output(self.number, GPIO.HIGH if value else GPIO.LOW)
        except:
            pass
        self.value = value

    def switch_value(self):
        try:
            GPIO.output(self.number, GPIO.LOW if self.value else GPIO.HIGH)
        except:
            pass
        self.value = not self.value


class Header:
    def __init__(self):
        self.left_pins = []
        self.right_pins = []
        for x in gpios:
            if x % 2 == 1:
                self.left_pins.append(Pin(x, False))
            else:
                self.right_pins.append(Pin(x, False))

    def get_value(self, number):
        for pin in self.left_pins + self.right_pins:
            if pin.number == number:
                return pin.value

    def set_value(self, number, value):
        for pin in self.left_pins + self.right_pins:
            if pin.number == number:
                pin.set_value(value)

    def switch_value(self, number):
        for pin in self.left_pins + self.right_pins:
            if pin.number == number:
                pin.switch_value()



header = Header()

try:
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(gpios, GPIO.OUT, initial=GPIO.LOW)
    print('Initialized GPIOs')
except:
    print('Could not set GPIO mode to BOARD.')