from dataclasses import dataclass, field
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
    def class_emoji(cls) -> str:
        pass

    @abstractmethod
    def emoji(self) -> str:
        pass

    def js(self) -> str:
        return f"replaceStyle('{self}', '{self.label()}')"


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
    def class_emoji(cls) -> str:
        return "🔅"

    def emoji(self) -> str:
        return "📺";



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
    def class_emoji(cls) -> str:
        return "🔍"

    def emoji(self) -> str:
        return "🔎"


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
    def class_emoji(cls) -> str:
        return "🖥"

    def emoji(self) -> str:
        return "💻"

    def js(self) -> str:
        return f"changePosition('{self}')"


class RenderAction(HtmlChoices):
    download = auto()

    @classmethod
    def default(cls) -> Self:
        return cast(Self, cls.download)

    @classmethod
    def label(cls) -> str:
        return "render"

    @classmethod
    def class_emoji(cls) -> str:
        return "💾"

    def emoji(self) -> str:
        return "🖨"

    def js(self) -> str:
        return f"window.print()"
