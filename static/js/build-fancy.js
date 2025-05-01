import { cap, withDiv, makeElement, addKids, maybeUpdateCss } from "./tools.js";

export const build = (data, color, size) => {
  maybeUpdateCss("format-style", "formats", "fancy");
  maybeUpdateCss("size-style", "sizes", size);
  maybeUpdateCss("color-style", "colors", color);

  document.getElementById("size-menu").style.display = "flex";
  document.getElementById("color-menu").style.display = "flex";

  const containerDiv = document.getElementById("container");
  containerDiv.replaceChildren(
    buildHeader(data),
    buildBottom(data),
  )
};

const buildHeader = data => {
  return withDiv({ id: "header" }, div => addKids(
    div,
    buildHeaderPhoto(data),
    buildHeaderInfo(data),
  ));
};

const buildHeaderPhoto = data => {
  return withDiv({ id: "header-photo" }, div => addKids(
    div,
    makeElement("img", { src: "static/images/me.png", alt: "Tucker Beck Photo" }),
  ));
};

const buildHeaderInfo = data => {
  return withDiv({ id: "header-info" }, div => addKids(
      div,
      buildHeaderTitle(data),
      buildHeaderContacts(data),
      buildHeaderSummary(data),
  ));
};

const buildHeaderTitle = data => {
  return withDiv({ id: "header-title" }, div => addKids(
      div,
      makeElement("h1", {id: "header-title-name", html: data.name}),
      makeElement("h2", {id: "header-title-role", html: data.role}),
  ));
};

const buildHeaderContacts = data => {
  return withDiv({ id: "header-contact-list" }, div => addKids(
    div,
    ...data.contacts.map(contact => withDiv({ klass: "header-contact-item" }, (cDiv) => addKids(
      cDiv,
      makeElement("p", {klass: "header-contact-emoji", html: contact.emoji}),
      makeElement("a", {klass: "header-contact-link", html: contact.text, href: contact.link, target: "_blank"}),
    ))),
  ));
};

const buildHeaderSummary = data => {
  return withDiv({ id: "header-summary" }, div => addKids(
    div,
    makeElement("p", {id: "header-summary-text", html: data.summary}),
  ));
};

const buildBottom = data => {
  return withDiv({ id: "bottom" }, div => addKids(
    div,
    buildSidebar(data),
    buildMain(data),
  ));
};

const buildSidebar = data => {
  return withDiv({ id: "sidebar" }, div => addKids(
    div,
    buildSkills(data),
    buildCerts(data),
    buildProjects(data),
  ));
};

const buildSkills = data => {
  return withDiv({ id: "skills", klass: "sidebar-item" }, div => addKids(
    div,
    makeElement("h2", { html: "Skills" }),
    ...["languages", "technologies", "platforms"].map(label => withDiv({ klass: "skills-item" }, sDiv => addKids(
      sDiv,
      makeElement("p", { klass: "skills-label", html: cap(label) + ":" }),
      makeElement("p", { klass: "skills-list", html: data.skills[label].join(", ") }),
    ))),
  ));
};

const buildCerts = data => {
  return withDiv({ id: "certs", klass: "sidebar-item" }, div => addKids(
    div,
    makeElement("h2", { html: "Certifications" }),
    ...data.certifications.map( (cert) => withDiv({ klass: "certs-item" }, cDiv => addKids(
      cDiv,
      makeElement("a", { klass: "certs-item-link", href: cert.link, target: "_blank", html: cert.abrv + ":" }),
      makeElement("p", { klass: "certs-item-date", html: cert.date }),
    ))),
  ));
};

const buildProjects = data => {
  return withDiv({ id: "projects", klass: "sidebar-item" }, div => addKids(
    div,
    makeElement("h2", { html: "Projects" }),
    ...data.projects.map( (project) => withDiv({ klass: "projects-item" }, (pDiv) => addKids(
      pDiv,
      makeElement("a", { klass: "projects-item-link", href: project.link, target: "_blank", html: project.name + ":" }),
      makeElement("p", { klass: "projects-item-description", html: project.summary }),
    ))),
  ));
};

const buildMain = data => {
  return withDiv({ id: "main" }, div => addKids(
    div,
    buildExp(data),
    buildEd(data),
  ));
};

const buildExp = data => {
  return withDiv({ id: "exp" }, div => addKids(
    div,
    makeElement("h2", { html: "Experience" }),
    ...data.experiences.map(exp => buildExpItem(exp) ),
  ));
};

const buildExpItem = exp => {
  return withDiv({ klass: "exp-item" }, div => addKids(
    div,
    buildExpTitle(exp),
    makeElement("p", { klass: "exp-item-date", html: exp.dates.start + " - " + exp.dates.end }),
    buildExpDetails(exp),
  ));
};

const buildExpTitle = exp => {
  return withDiv({ klass: "exp-item-title" }, div => addKids(
    div,
    makeElement("a", { klass: "exp-item-company", href: exp.link, target: "_blank", html: exp.company + ":" }),
    makeElement("p", { klass: "exp-item-role", html: exp.role }),
  ));
};

const buildExpDetails = exp => {
  return withDiv({ klass: "exp-item-details" }, div => addKids(
    div,
    addKids(
      makeElement("ul", { klass: "exp-item-details-list" }),
      ...exp.details.map(detail => {
        exp.links.map(link => {
          detail = detail.replace(link.pattern, `<a href="${ link.href }" target="_blank">${ link.pattern }</a>`);
        });
        return makeElement("li", { klass: "exp-item-details-item", html: detail });
      }),
    ),
  ));
};

const buildEd = data => {
  return withDiv({ id: "education" }, div => addKids(
    div,
    makeElement("h2", { html: "Education" }),
    withDiv({ id: "education-title" }, tDiv => addKids(
      tDiv,
      makeElement("a", { id: "education-title-school", href: data.education.link, target: "_blank", html: data.education.school + ":" }),
      makeElement("p", { id: "education-title-degree", html: data.education.degree }),
    )),
    makeElement("p", { id: "education-dates", html: data.education.dates.start + " - " + data.education.dates.end }),
    withDiv({ id: "education-details" }, dDiv => addKids(
      dDiv,
      addKids(
        makeElement("ul", { id: "education-details-list" }),
        ...data.education.details.map(detail => makeElement(
          "li", { klass: "education-details-item", html: detail },
        )),
      ),
    )),
  ));
};
