import { cap } from "./tools.js";

export const build = (data) => {
  const formatCssUrl = "static/css/formats/plain.css";
  const oldFormatCss = document.getElementById("format-css");
  if (oldFormatCss.href !== formatCssUrl) {
    const newFormatCss = document.createElement("link");
    newFormatCss.setAttribute("id", "format-css");
    newFormatCss.setAttribute("rel", "stylesheet");
    newFormatCss.setAttribute("type", "text/css");
    newFormatCss.setAttribute("href", formatCssUrl);

    oldFormatCss.replaceWith(newFormatCss);
  }

  const sizeStyle = document.getElementById("size-style")
  if (sizeStyle !== null) {
    sizeStyle.remove()
  }
  const colorStyle = document.getElementById("color-style")
  if (colorStyle !== null) {
    colorStyle.remove()
  }

  document.getElementById("size-menu").style.display = "none";
  document.getElementById("color-menu").style.display = "none";

  const containerDiv = document.getElementById("container");
  containerDiv.replaceChildren(
    buildHeader(data),
    buildSkills(data),
    buildCerts(data),
    buildExperiences(data),
    buildProjects(data),
    buildEducation(data),
  )
}

const buildHeader = (data) => {
  const headerDiv = document.createElement("div");
  headerDiv.setAttribute("id", "header");
  headerDiv.appendChild(buildHeaderTitle(data));
  headerDiv.appendChild(buildHeaderContacts(data));
  headerDiv.appendChild(buildHeaderSummary(data));
  return headerDiv;
}

const buildHeaderTitle = (data) => {
  const titleDiv = document.createElement("div");
  titleDiv.setAttribute("id", "header-title");

  const titleName = document.createElement("h1");
  titleName.innerHTML = data.name;
  titleName.setAttribute("id", "header-title-name");
  titleDiv.appendChild(titleName);

  const titleSep = document.createElement("h1");
  titleSep.innerHTML = "-";
  titleSep.setAttribute("id", "header-title-sep");
  titleDiv.appendChild(titleSep);

  const titleRole = document.createElement("h1");
  titleRole.innerHTML = data.role;
  titleRole.setAttribute("id", "header-title-role");
  titleDiv.appendChild(titleRole);

  return titleDiv;
}

const buildHeaderContacts = (data) => {
  const contactsDiv = document.createElement("div");
  contactsDiv.setAttribute("id", "header-contact-list");

  data.contacts.forEach(contact => {
    const contactDiv = document.createElement("div");
    contactDiv.setAttribute("class", "header-contact");

    const contactEmoji = document.createElement("p");
    contactEmoji.setAttribute("class", "header-contact-emoji");
    contactEmoji.innerHTML = contact.emoji;
    contactDiv.appendChild(contactEmoji);

    const contactLink = document.createElement("a");
    contactLink.setAttribute("class", "header-contact-link");
    contactLink.setAttribute("href", contact.link);
    contactLink.setAttribute("target", "_blank");
    contactLink.innerHTML = contact.text;
    contactDiv.appendChild(contactLink);

    contactsDiv.appendChild(contactDiv);
  })
  return contactsDiv;
}

const buildHeaderSummary = (data) => {
  const summaryDiv = document.createElement("div");
  summaryDiv.setAttribute("id", "header-summary");

  const summaryText = document.createElement("p");
  summaryText.setAttribute("id", "header-summary");
  summaryText.innerHTML = data.summary;
  summaryDiv.appendChild(summaryText);

  return summaryDiv;
}

const buildSkills = (data) => {
  const skillsDiv = document.createElement("div");
  skillsDiv.setAttribute("id", "skills");

  const skillsTitle = document.createElement("h2");
  skillsTitle.innerHTML = "Skills"
  skillsDiv.appendChild(skillsTitle);

  skillsDiv.appendChild(buildSkillsItem("languages", data));
  skillsDiv.appendChild(buildSkillsItem("technologies", data));
  skillsDiv.appendChild(buildSkillsItem("platforms", data));

  return skillsDiv;
}

const buildSkillsItem = (label, data) => {
  const sectionDiv = document.createElement("div");
  sectionDiv.setAttribute("class", "skills-item");

  const sectionLabel = document.createElement("p");
  sectionLabel.setAttribute("class", "skills-label");
  sectionLabel.innerHTML = cap(label) + ":";
  sectionDiv.appendChild(sectionLabel);

  const sectionList = document.createElement("p");
  sectionList.setAttribute("class", "skills-list");
  sectionList.innerHTML = data.skills[label].join(", ");
  sectionDiv.appendChild(sectionList);

  return sectionDiv;
}

const buildCerts = (data) => {
  const certsDiv = document.createElement("div");
  certsDiv.setAttribute("id", "certs");

  const certsTitle = document.createElement("h2");
  certsTitle.innerHTML = "Certifications"
  certsDiv.appendChild(certsTitle);

  data.certifications.forEach(cert => {
    const certDiv = document.createElement("div");
    certDiv.setAttribute("class", "certs-item");

    const certLink = document.createElement("a");
    certLink.setAttribute("class", "certs-item-link");
    certLink.setAttribute("href", cert.link);
    certLink.setAttribute("target", "_blank");
    certLink.innerHTML = cert.name;
    certDiv.appendChild(certLink);

    const certDate = document.createElement("p");
    certDate.setAttribute("class", "certs-item-date");
    certDate.innerHTML = cert.date;
    certDiv.appendChild(certDate);

    certsDiv.appendChild(certDiv);
  })

  return certsDiv;
}

const buildExperiences = (data) => {
  const expDiv = document.createElement("div");
  expDiv.setAttribute("id", "exp");

  const expTitle = document.createElement("h2");
  expTitle.innerHTML = "Experience"
  expDiv.appendChild(expTitle);

  data.experiences.map(exp => {
    expDiv.appendChild(buildExp(exp));
  })

  return expDiv;
}

const buildExp = (exp) => {
  const expItemDiv = document.createElement("div");
  expItemDiv.setAttribute("class", "exp-item");

  expItemDiv.appendChild(buildExpTitle(exp));
  expItemDiv.appendChild(buildExpDetails(exp));

  return expItemDiv;
}

const buildExpTitle = (exp) => {
  const expTitleDiv = document.createElement("div");
  expTitleDiv.setAttribute("class", "exp-item-title");

  const expTitleLeftDiv = document.createElement("div");
  expTitleLeftDiv.setAttribute("class", "exp-item-title-left");

  const expTitleCompany = document.createElement("a");
  expTitleCompany.setAttribute("class", "exp-item-company");
  expTitleCompany.setAttribute("href", exp.link);
  expTitleCompany.setAttribute("target", "_blank");
  expTitleCompany.innerHTML = exp.company + ":";
  expTitleLeftDiv.appendChild(expTitleCompany);

  const expTitleRole = document.createElement("p");
  expTitleRole.setAttribute("class", "exp-item-role");
  expTitleRole.innerHTML = exp.role;
  expTitleLeftDiv.appendChild(expTitleRole);

  expTitleDiv.appendChild(expTitleLeftDiv);

  const expTitleRightDiv = document.createElement("div");
  expTitleRightDiv.setAttribute("class", "exp-item-title-right");

  const expTitleDates = document.createElement("p");
  expTitleDates.setAttribute("class", "exp-item-dates");
  expTitleDates.innerHTML = exp.dates.start + " - " + exp.dates.end;
  expTitleRightDiv.appendChild(expTitleDates);

  expTitleDiv.appendChild(expTitleRightDiv);

  return expTitleDiv;
}

const buildExpDetails = (exp) => {
  const expDetailsDiv = document.createElement("div");
  expDetailsDiv.setAttribute("class", "exp-item-details");

  const expDetailsList = document.createElement("ul");
  expDetailsList.setAttribute("class", "exp-item-details-list");
  exp.details.map(detail => {
    expDetailsList.appendChild(buildExpDetailItem(detail, exp.links));
  });
  expDetailsDiv.appendChild(expDetailsList);

  return expDetailsDiv;
}

const buildExpDetailItem = (detail, links) => {
  links.forEach(link => {
    detail = detail.replace(link.pattern, `<a href="${link.href}" target="_blank">${link.pattern}</a>`);
  });

  const expDetailItem = document.createElement("li");
  expDetailItem.setAttribute("class", "exp-item-details-item");
  expDetailItem.innerHTML = detail;
  return expDetailItem;
}

const buildProjects = (data) => {
  const projectsDiv = document.createElement("div");
  projectsDiv.setAttribute("id", "projects");

  const projectsDivTitle = document.createElement("h2");
  projectsDivTitle.innerHTML = "Projects";
  projectsDiv.appendChild(projectsDivTitle);

  data.projects.forEach(project => {
    projectsDiv.appendChild(buildProjectItem(project));
  });

  return projectsDiv;
}

const buildProjectItem = (project) => {
  const projectDiv = document.createElement("div");
  projectDiv.setAttribute("class", "projects-item");

  const projectTitleDiv = document.createElement("div");
  projectTitleDiv.setAttribute("class", "projects-item-title");

  const projectLink = document.createElement("a");
  projectLink.setAttribute("class", "projects-item-link");
  projectLink.setAttribute("href", project.link);
  projectLink.setAttribute("target", "_blank");
  projectLink.innerHTML = project.name + ":";
  projectTitleDiv.appendChild(projectLink);

  const projectDescription = document.createElement("p");
  projectDescription.setAttribute("class", "projects-item-description");
  projectDescription.innerHTML = project.summary;
  projectTitleDiv.appendChild(projectDescription);

  projectDiv.appendChild(projectTitleDiv);

  projectDiv.appendChild(buildProjectDetails(project));

  return projectDiv;
}

const buildProjectDetails = (project) => {
  const projectDetailsDiv = document.createElement("div");
  projectDetailsDiv.setAttribute("class", "projects-item-details");

  const projectDetailsList = document.createElement("ul");
  projectDetailsList.setAttribute("class", "projects-item-details-list");
  project.details.map(detail => {
    const projectDetailItem = document.createElement("li");
    projectDetailItem.setAttribute("class", "projects-item-details-item");
    projectDetailItem.innerHTML = detail;
    projectDetailsList.appendChild(projectDetailItem);
  });
  projectDetailsDiv.appendChild(projectDetailsList);

  return projectDetailsDiv;
}

const buildEducation = (data) => {
  const edDiv = document.createElement("div");
  edDiv.setAttribute("id", "education");

  const edTitle = document.createElement("h2");
  edTitle.innerHTML = "Education";
  edDiv.appendChild(edTitle);

  const edTitleDiv = document.createElement("div");
  edTitleDiv.setAttribute("class", "education-title");
  edDiv.appendChild(edTitleDiv);

  const edTitleLeft = document.createElement("div");
  edTitleLeft.setAttribute("class", "education-title-left")
  edTitleDiv.appendChild(edTitleLeft)

  const edTitleSchool = document.createElement("a");
  edTitleSchool.setAttribute("class", "education-title-school");
  edTitleSchool.setAttribute("href", data.education.link);
  edTitleSchool.setAttribute("target", "_blank");
  edTitleSchool.innerHTML = data.education.school + ":";
  edTitleLeft.appendChild(edTitleSchool);

  const edTitleDegree = document.createElement("p");
  edTitleDegree.setAttribute("class", "education-title-degree");
  edTitleDegree.innerHTML = data.education.degree;
  edTitleLeft.appendChild(edTitleDegree);

  const edTitleRight = document.createElement("div");
  edTitleRight.setAttribute("class", "education-title-right")
  edTitleDiv.appendChild(edTitleRight)

  const edTitleDates = document.createElement("p");
  edTitleDates.setAttribute("class", "education-title-dates");
  edTitleDates.innerHTML = data.education.dates.start + " - " + data.education.dates.end;
  edTitleRight.appendChild(edTitleDates);

  edDiv.appendChild(edTitleDiv);
  edDiv.appendChild(buildEducationDetails(data.education));

  return edDiv;
}

const buildEducationDetails = (ed) => {
  const edDetailsDiv = document.createElement("div");
  edDetailsDiv.setAttribute("class", "education-details");

  const edDetailsList = document.createElement("ul");
  edDetailsList.setAttribute("class", "education-details-list");
  ed.details.map(detail => {
    const edDetailItem = document.createElement("li");
    edDetailItem.setAttribute("class", "education-details-item");
    edDetailItem.innerHTML = detail;
    edDetailsList.appendChild(edDetailItem);
  });
  edDetailsDiv.appendChild(edDetailsList);

  return edDetailsDiv;
}
