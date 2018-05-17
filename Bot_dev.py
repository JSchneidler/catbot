import struct

class Bot:
    def __init__(self):
        self.speed = 0;
        self.speedLeft = 1;
        self.speedRight = 1;
        self.direction = 0;

    def processCommand(self, command):
        speed, direction = struct.unpack('bb', command);

        print(speed, direction);

        '''
        if speed != self.speed:
            self.updateSpeed(speed);

        if direction != self.direction:
            self.updateDirection(direction);
        '''

    def updateSpeed(self, speed):
        self.speed = abs(speed)/100;

        if speed == 0: self.stop();
        elif speed < 0: self.reverse();
        else: self.forward();

    def updateDirection(self, direction):
        self.direction = direction;

        # Turning left
        if direction < 0:
            self.speedRight = 1;
            self.speedLeft = abs(direction) / 90;
            self.turnLeft();

        # Turning right
        elif direction > 0:
            self.speedLeft = 1;
            self.speedRight = abs(direction) / 90;
            self.turnRight();

        # Going straight
        else: self.forward();

    def leftMotorForward(self, speed = None):
        if not speed: speed = self.speed;
        print('leftForwardSpeed' + str(speed));
        self.leftMotorEnable.value = speed;
        self.leftMotorDirection1.on();
        self.leftMotorDirection2.off();

    def rightMotorForward(self, speed = None):
        if not speed: speed = self.speed;
        print('rightForwardSpeed' + str(speed));
        self.rightMotorEnable.value = speed;
        self.rightMotorDirection1.on();
        self.rightMotorDirection2.off();

    def forward(self):
        self.leftMotorForward();
        self.rightMotorForward();

    def leftMotorReverse(self, speed = None):
        if not speed: speed = self.speed;
        print('leftReverseSpeed' + str(speed));
        self.leftMotorEnable.value = speed;
        self.leftMotorDirection1.off();
        self.leftMotorDirection2.on();

    def rightMotorReverse(self, speed = None):
        if not speed: speed = self.speed;
        print('rightReverseSpeed' + str(speed));
        self.rightMotorEnable.value = speed;
        self.rightMotorDirection1.off();
        self.rightMotorDirection2.on();

    def reverse(self):
        self.leftMotorReverse();
        self.rightMotorReverse();

    def leftMotorStop(self):
        self.leftMotorEnable.off();

    def rightMotorStop(self):
        self.rightMotorEnable.off();

    def stop(self):
        self.leftMotorStop();
        self.rightMotorStop();

    def turnLeft(self):
        self.leftMotorReverse(self.speedLeft * self.speed);
        self.rightMotorForward(self.speedRight * self.speed);

    def turnRight(self):
        self.leftMotorForward(self.speedLeft * self.speed);
        self.rightMotorReverse(self.speedRight * self.speed);
