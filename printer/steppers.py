import atexit
from Adafruit_MotorHAT import Adafruit_MotorHAT


class Stepper:
    def __init__(self, stepper):
        self.name = stepper['name']
        self.step = stepper['step']
        self.speed = stepper['speed']

class Hat:
    def __init__(self, hat):
        self.addr = hat['addr']
        self.freq = hat['freq']
        self.mh = Adafruit_MotorHAT(addr=hat['addr'], freq=hat['freq'])
        atexit.register(self.__turnOffMotors)

    def __turnOffMotors(self):
        self.mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
        self.mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
        self.mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
        self.mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)