from cv.schemas import CV


def build(cv: CV) -> str:
    parts: list[str] = []

    parts.append(f"# {cv.main.name} - {cv.main.role}")
    parts.append("")
    contacts_parts: list[str] = []
    for contact in cv.main.contacts:
        contacts_parts.append(f"{contact.emoji} [{contact.text}]({contact.link})")
    parts.append(" | ".join(contacts_parts))
    parts.append("")
    parts.append(cv.main.summary)
    parts.append("")
    parts.append("")

    parts.append("## Skills")
    parts.append("")
    parts.append(f"- **Languages:** {', '.join(cv.main.skills.languages)}")
    parts.append(f"- **Technologies:** {', '.join(cv.main.skills.technologies)}")
    parts.append(f"- **Platforms:** {', '.join(cv.main.skills.platforms)}")
    parts.append("")
    parts.append("")

    parts.append("## Certs")
    parts.append("")
    for cert in cv.main.certifications:
        parts.append(f"- **[{cert.abrv}]({cert.link}):** {cert.date}")
    parts.append("")
    parts.append("")

    parts.append("## Projects")
    parts.append("")
    for project in cv.main.projects:
        parts.append(f"- **[{project.name}]({project.link}):** {project.summary}")
    parts.append("")
    parts.append("")

    parts.append("## Experience")
    parts.append("")
    for exp in cv.main.experiences:
        parts.append(f"### {exp.dates.start} - {exp.dates.end}: [{exp.company}]({exp.link})")
        parts.append(f"#### {exp.role}")
        parts.append("")
        for text in exp.details:
            for link in exp.links:
                text = text.replace(link.pattern, f"[{link.pattern}]({link.href})")
            parts.append(f"- {text}")
        parts.append("")
        parts.append("")

    parts.append("## Education")
    parts.append("")
    parts.append(f"### {cv.main.education.dates.start} - {cv.main.education.dates.end}: [{cv.main.education.school}]({cv.main.education.link})")
    parts.append("")
    parts.append(f"#### {cv.main.education.degree}")
    parts.append("")
    for detail in cv.main.education.details:
        parts.append(f"- {detail}")

    return "\n".join([p.strip() for p in parts])
