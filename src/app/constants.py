from auto_name_enum import AutoNameEnum, auto


class ColorScheme(AutoNameEnum):
    light = auto()
    night = auto()
    blue = auto()
    bold = auto()


DEFAULT_COLOR = ColorScheme.light
