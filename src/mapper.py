from evdev import ecodes


class Mapper:
    # taken from https://github.com/torvalds/linux/blob/master/include/uapi/linux/input-event-codes.h
    mapping = {
        "0": ecodes.KEY_T,
        "2": ecodes.KEY_UP,
        "4": ecodes.KEY_LEFT,
        "5": ecodes.KEY_SPACE,
        "6": ecodes.KEY_RIGHT,
        "8": ecodes.KEY_DOWN,
    }

    def keycode_from_number(self, number):
        return Mapper.mapping[number]
