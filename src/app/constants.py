from typing import Self, cast
from abc import abstractmethod
from enum import StrEnum, auto


class HtmlChoices(StrEnum):

    @classmethod
    @abstractmethod
    def default(cls) -> Self:
        pass


    @classmethod
    @abstractmethod
    def label(cls) -> str:
        pass


    @classmethod
    @abstractmethod
    def emoji(cls) -> str:
        pass

    def js(self) -> str:
        return f"replaceStyle({self}, {self.label()})"


class ColorScheme(HtmlChoices):
    light = auto()
    night = auto()
    blue = auto()
    bold = auto()

    @classmethod
    def default(cls) -> Self:
        return cast(Self, cls.light)

    @classmethod
    def label(cls) -> str:
        return "color"

    @classmethod
    def emoji(cls) -> str:
        return "🔅"



class Size(HtmlChoices):
    small = auto()
    medium = auto()
    large = auto()

    @classmethod
    def default(cls) -> Self:
        return cast(Self, cls.medium)

    @classmethod
    def label(cls) -> str:
        return "size"

    @classmethod
    def emoji(cls) -> str:
        return "🔍"

    def js(self) -> str:
        return f"replaceStyle({self}, {self.label()})"


class Position(HtmlChoices):
    manager = auto()
    staff = auto()
    senior = auto()

    @classmethod
    def default(cls) -> Self:
        return cast(Self, cls.staff)

    @classmethod
    def label(cls) -> str:
        return "position"

    @classmethod
    def emoji(cls) -> str:
        return "🖥"

    def js(self) -> str:
        return f"changePosition('{self}')"


class RenderAction(HtmlChoices):
    download = auto()
    printer = auto()

    @classmethod
    def default(cls) -> Self:
        return cast(Self, cls.printer)

    @classmethod
    def label(cls) -> str:
        return "render"

    @classmethod
    def emoji(cls) -> str:
        return "🖨"

    def js(self) -> str:
        return f"window.print()"
