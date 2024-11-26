import logging

from evdev import ecodes


logger = logging.getLogger(__name__)


class PhoneBoard:
    def __init__(self, uinput, mapper):
        self.keyboard = Keyboard(uinput)
        self.mapper = mapper

    def keystroke(self, number):
        try:
            keycode = self.mapper.keycode_from_number(number)
        except KeyError:
            logger.warning(f'unable to map number: {number}')
            return

        self.keyboard.keystroke(keycode)


class Keyboard:
    def __init__(self, uinput):
        self.uinput = uinput

    def keystroke(self, keycode):
        self.uinput.write(ecodes.EV_KEY, keycode, 1)
        self.uinput.write(ecodes.EV_KEY, keycode, 0)
        self.uinput.syn()
