from pathlib import Path
from typing import Self, Any

import yaml
from pydantic import BaseModel, HttpUrl, AnyUrl


class Contact(BaseModel):
    text: str
    link: AnyUrl
    emoji: str


class Skills(BaseModel):
    languages: list[str]
    technologies: list[str]
    platforms: list[str]


class Certification(BaseModel):
    name: str
    abrv: str
    link: HttpUrl
    date: str


class Project(BaseModel):
    name: str
    summary: str
    link: HttpUrl
    details: list[str]


class DateRange(BaseModel):
    start: str
    end: str


class ExperienceLink(BaseModel):
    pattern: str
    href: HttpUrl


class Experience(BaseModel):
    company: str
    link: HttpUrl
    role: str
    dates: DateRange
    details: list[str]
    links: list[ExperienceLink]


class Education(BaseModel):
    school: str
    link: HttpUrl
    degree: str
    dates: DateRange
    details: list[str]


class Data(BaseModel):
    name: str
    role: str
    contacts: list[Contact]
    summary: str
    skills: Skills
    certifications: list[Certification]
    projects: list[Project]
    experiences: list[Experience]
    education: Education


class CV(BaseModel):
    main: Data
    profiles: dict[str, Any]  # This is a bit of a hack. Would be nicer if Pydantic had partials

    @classmethod
    def parse(cls, path: Path) -> Self:
        text = path.read_text()
        data = yaml.safe_load(text)
        return cls(**data)

    def dump(self, path: Path):
        path.write_text(self.model_dump_json(indent=2))
