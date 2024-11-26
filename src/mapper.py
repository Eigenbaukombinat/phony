from evdev import ecodes


class Mapper:
    mapping = {
        "0": ecodes.KEY_KP2,
        "1": ecodes.KEY_A,
        "2": ecodes.KEY_B,
        "3": ecodes.KEY_C,
        "#": ecodes.KEY_D,
    }

    def keycode_from_number(self, number):
        return Mapper.mapping[number]
