import asyncio
import logging

from evdev import ecodes


logger = logging.getLogger(__name__)


class PhoneBoard:
    def __init__(self, uinput, mapper):
        self.keyboard = Keyboard(uinput)
        self.mapper = mapper

    async def keystroke(self, number):
        try:
            keycode = self.mapper.keycode_from_number(number)
        except KeyError:
            logger.warning(f"unable to map number: {number}")
            return

        await self.keyboard.keystroke(keycode)


class Keyboard:
    def __init__(self, uinput):
        self.uinput = uinput

    async def keystroke(self, keycode):
        self.uinput.write(ecodes.EV_KEY, keycode, 1)
        self.uinput.syn()
        await asyncio.sleep(0.2)
        self.uinput.write(ecodes.EV_KEY, keycode, 0)
        self.uinput.syn()
