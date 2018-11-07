from models import Dispenser
from nanpy import Stepper
from nanpy import SerialManager
from nanpy import ArduinoApi


class ArduinoModule:
    def __init__(self, *args, **kwargs):
        self.device = kwargs.get('device')
        self.connection = kwargs.get('connection')
        if self.connection is None:
            self.connection = SerialManager(self.device)
            self.api = ArduinoApi(connection=self.connection)


class Infrared(ArduinoModule):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.outPin = kwargs.get('outPin')

    def detect(self):
        return self.api.digitalRead(int(self.outPin)) == 1


class Rack(Stepper, ArduinoModule):
    def __init__(self, revsteps, pin1, pin2, speed=None, connection=None, pin3=None, pin4=None, *args, **kwargs):
        Stepper.__init__(self, revsteps, pin1, pin2,
                         speed, connection, pin3, pin4)
        ArduinoModule.__init__(self, *args, **kwargs)
        self.infrared = Infrared(pin=kwargs.get('infrared'))
        self.speed = kwargs.get('speed')
        self.setSpeed(self.speed)

    def run(self):
        while not self.infrared.detect():
            self.setSpeed(self.speed)
            self.step(1)


class Machine(Dispenser, ArduinoModule):
    def __init__(self, *args, **kwargs):
        Dispenser.__init__(self, *args, **kwargs)
        ArduinoModule.__init__(self, *args, **kwargs)
        self.racks = {}
        for i, inventory in enumerate(self.inventories):
            pin1 = i + 1
            pin2 = i + 2
            pin3 = i + 3
            pin4 = i + 4
            rack = Rack(revsteps=100, pin1=pin1, pin2=pin2, pin3=pin3, pin4=pin4, connection=self.connection)
            self.racks[inventory.id](rack)
    def dispense(self, **kwargs):
        super().dispense(**kwargs)
        rack = self.racks[kwargs.get('inventory')]
        rack.run()
