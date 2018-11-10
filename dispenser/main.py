from nanpy import ArduinoApi, SerialManager, Stepper

serial = SerialManager(device='/dev/ttyACM0')

motor = Stepper(
    revsteps=3800,
    pin1=1,
    pin2=2,
    pin3=3,
    pin4=4,
    connection=serial,
    speed=10
)

x = 100

while True:
    x = x + 100
    motor.step(x)