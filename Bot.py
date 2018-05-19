from gpiozero import DigitalOutputDevice, PWMOutputDevice
import struct

LEFT_MOTOR_ENABLE_PIN = 12;
LEFT_MOTOR_IN1_PIN = 8;
LEFT_MOTOR_IN2_PIN = 7;

RIGHT_MOTOR_ENABLE_PIN = 18;
RIGHT_MOTOR_IN1_PIN = 23;
RIGHT_MOTOR_IN2_PIN = 24;

DIRECTIONS = {
    '0': [1, 1],
    '45': [1, 0.5],
    '90': [1, -1],
    '135': [-1, -0.5],
    '180': [-1, -1],
    '-135': [-0.5, -1],
    '-90': [-1, 1],
    '-45': [0.5, 1]
};

class Bot:
    def __init__(self):
        self.leftMotorEnable = PWMOutputDevice(LEFT_MOTOR_ENABLE_PIN);
        self.leftMotorDirection1 = DigitalOutputDevice(LEFT_MOTOR_IN1_PIN);
        self.leftMotorDirection2 = DigitalOutputDevice(LEFT_MOTOR_IN2_PIN);
        self.rightMotorEnable = PWMOutputDevice(RIGHT_MOTOR_ENABLE_PIN);
        self.rightMotorDirection1 = DigitalOutputDevice(RIGHT_MOTOR_IN1_PIN);
        self.rightMotorDirection2 = DigitalOutputDevice(RIGHT_MOTOR_IN2_PIN);

        self.speed = 0;
        self.speedLeft = 0;
        self.speedRight = 0;
        self.direction = 0;

    def processCommand(self, command):
        speed, direction = struct.unpack('>Hh', command);

        print(speed, direction);

        self.updateBot(speed, direction);

    def updateBot(self, speed, direction):
        self.speed = speed;
        self.direction = direction;

        if speed == 0: self.stop();
        else:
            self.speedLeft = DIRECTIONS[str(direction)][0] * (self.speed/100);
            self.speedRight = DIRECTIONS[str(direction)][1] * (self.speed/100);

            self.setLeftMotorSpeed(self.speedLeft);
            self.setRightMotorSpeed(self.speedRight);

    def setLeftMotorSpeed(self, speed):
        print('leftForwardSpeed' + str(speed));
        self.leftMotorEnable.value = abs(speed);
        if speed > 0:
            self.leftMotorDirection1.on();
            self.leftMotorDirection2.off();
        else:
            self.leftMotorDirection1.off();
            self.leftMotorDirection2.on();

    def setRightMotorSpeed(self, speed):
        print('rightForwardSpeed' + str(speed));
        self.rightMotorEnable.value = abs(speed);
        if speed > 0:
            self.rightMotorDirection1.on();
            self.rightMotorDirection2.off();
        else:
            self.rightMotorDirection1.off();
            self.rightMotorDirection2.on();

    def leftMotorStop(self):
        self.leftMotorEnable.off();

    def rightMotorStop(self):
        self.rightMotorEnable.off();

    def stop(self):
        self.leftMotorStop();
        self.rightMotorStop();