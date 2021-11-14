#This code runs on Raspberry Pi Pico via MicroPython
import machine
import time
from machine import Timer

signal = {
    'ROW_ENABLE': 0, 'ROW_DISABLE': 1,
    'COL_ENABLE': 1, 'COL_DISABLE': 0
}

rowpin  = (11, 10,  9,  8,  7,  6)
colpin  = ( 0,  1,  2,  3,  4,  5)

rowpins = []
colpins = []

world = (
    (0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0),
    (0, 0, 1, 1, 0, 0),
    (0, 1, 0, 0, 1, 0),
    (1, 0, 0, 0, 0, 1),
)


class Element():
    def __init__(self, rows):
        self.rows = rows
        self.pos = 0

    def move(self):
        self.pos = (self.pos + 1) % self.rows


class Field(Element):
    def __init__(self, world):
        super().__init__(len(world))
        self.world = world

    def map(self, view):
        line = (self.pos + view.pos) % self.rows
        return self.world[line]


class View(Element):
    def __init__(self, rows):
        super().__init__(rows)


field = Field(world)


def animation(timer):
    field.move()


def setup():
    for i in range(len(rowpin)):
        rowpins.append(machine.Pin(rowpin[i], machine.Pin.OUT))
        rowpins[i].value(signal['ROW_DISABLE'])

    for i in range(len(colpin)):
        colpins.append(machine.Pin(colpin[i], machine.Pin.OUT))
        colpins[i].value(signal['COL_DISABLE'])

    tim = Timer()
    tim.init(freq = 1, mode = Timer.PERIODIC, callback = animation)


def loop():
    view = View(len(rowpin))

    while True:
        rowpins[view.pos].value(signal['ROW_DISABLE'])
        map = field.map(view)
        for c in range(len(colpins)):
            colpins[c].value(map[c])
        rowpins[view.pos].value(signal['ROW_ENABLE'])
        time.sleep(1/1000)
        rowpins[view.pos].value(signal['ROW_DISABLE'])

        view.move()


if __name__ == '__main__':
    setup()
    loop()
