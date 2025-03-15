from auto_name_enum import AutoNameEnum, auto


class ColorScheme(AutoNameEnum):
    light = auto()
    night = auto()
    blue = auto()
    bold = auto()


DEFAULT_COLOR = ColorScheme.light


class Size(AutoNameEnum):
    small = auto()
    medium = auto()
    large = auto()


DEFAULT_SIZE = Size.medium
