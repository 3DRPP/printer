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
        self.left_pins.append(Pin(3, False))
        self.left_pins.append(Pin(5, False))
        self.left_pins.append(Pin(7, False))
        self.left_pins.append(Pin(11, False))
        self.left_pins.append(Pin(13, False))
        self.left_pins.append(Pin(15, False))
        self.left_pins.append(Pin(19, False))
        self.left_pins.append(Pin(21, False))
        self.left_pins.append(Pin(23, False))
        self.left_pins.append(Pin(29, False))
        self.left_pins.append(Pin(31, False))
        self.left_pins.append(Pin(33, False))
        self.left_pins.append(Pin(35, False))
        self.left_pins.append(Pin(37, False))
        self.right_pins = []
        self.right_pins.append(Pin(8, False))
        self.right_pins.append(Pin(10, False))
        self.right_pins.append(Pin(12, False))
        self.right_pins.append(Pin(16, False))
        self.right_pins.append(Pin(18, False))
        self.right_pins.append(Pin(22, False))
        self.right_pins.append(Pin(24, False))
        self.right_pins.append(Pin(26, False))
        self.right_pins.append(Pin(32, False))
        self.right_pins.append(Pin(36, False))
        self.right_pins.append(Pin(38, False))
        self.right_pins.append(Pin(40, False))

    def get_value(self, number):
        for pin in self.left_pins + self.right_pins:
            if pin.number == number:
                return pin.value

    def set_value(self, number, value):
        for pin in self.left_pins + self.right_pins:
            if pin.number == number:
                pin.set_value(value)

    def switch_value(self, number):
        print('here')
        for pin in self.left_pins + self.right_pins:
            print(pin.number)
            if pin.number == number:
                print('ok')
                pin.switch_value()



header = Header()

try:
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(gpios, GPIO.OUT, initial=GPIO.LOW)
    print('Initialized GPIOs')
except:
    print('Could not set GPIO mode to BOARD.')