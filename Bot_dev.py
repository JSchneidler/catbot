import struct

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

        if speed == 0:
            print('stopped');
            #self.stop();
        else:
            self.speedLeft = DIRECTIONS[str(direction)][0] * (self.speed/100);
            self.speedRight = DIRECTIONS[str(direction)][1] * (self.speed/100);

            print(self.speedLeft);
            print(self.speedRight);
            '''
            self.setLeftMotorSpeed(self.speedLeft);
            self.setRightMotorSpeed(self.speedRight);
            '''

