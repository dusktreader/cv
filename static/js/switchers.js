const titles = {
    "manager": {
        "position": "Engineering Manager",
        "summary": "I'm an Engineering Leader focused on assembling powerhouse dev teams that consistently deliver high-impact software solutions. I lead with a fusion of empathy and resolve; it's my mission to deeply understand my people, the problems we face, and pragmatic strategies built on our strengths. Building a culture of determined collaboration and fearless innovation is crucial for the journey ahead. I'm committed to building teams where partnership, expertise, and tenacity are at the core of everything we do."
    },
    "staff": {
        "position": "Staff Software Engineer",
    },
    "senior": {
        "position": "Senior Software Engineer",
    }
}

window.onload = () => {
  var sumElement = document.getElementById("summary")
  children = sumElement.children
  Array.from(children).forEach((child) => {
    if (child.tagName === "P") {
      text = child.innerHTML
      console.log("Setting default summary")
      localStorage.setItem("defaultSummary", child.innerHTML)
    }
  });
}

const head = document.getElementsByTagName('head')[0];

const replaceStyle = (name, label) => {
  console.log(`Chosen ${label}: ${name}`);
  var style = document.getElementById(`${label}-style`);
  style.remove();

  const path = `static/css/${label}s/${name}.css`;

  style = document.createElement('link');
  style.setAttribute('rel', 'stylesheet');
  style.setAttribute('type', 'text/css');
  style.setAttribute('id', `${label}-style`);
  style.setAttribute('href', path);
  head.appendChild(style);
};

const changePosition = (key) => {
  console.log(`Changing position to ${key}`)
  var posElement = document.getElementById("title-position");
  var sumElement = document.getElementById("summary")

  var summaryText = titles[key].summary
  if (!summaryText) {
    console.log("Using default summary")
    summaryText = localStorage.getItem("defaultSummary");
  }
  if (!summaryText) {
    console.log("No default summary found")
    summaryText = "<i>Couldn't load default summary from local storage. Please refresh page<i>"
  }
  posElement.innerHTML = titles[key].position
  sumElement.innerHTML = `<p>${summaryText}</p>`
}

const showDiv = (id) => {

  Array.from(document.getElementsByClassName("switcher-buttons")).map(e => {
    e.style.removeProperty('display');
  });

  if (id !== undefined) {
    document.getElementById(id).style.display = "flex";
  }
};

const positionMenu = document.getElementById('position-menu');
positionMenu.addEventListener('mouseover', () => showDiv("position-buttons"));

const colorMenu = document.getElementById('color-menu');
colorMenu.addEventListener('mouseover', () => showDiv("color-buttons"));

const sizeMenu = document.getElementById('size-menu');
sizeMenu.addEventListener('mouseover', () => showDiv("size-buttons"));

const renderMenu = document.getElementById('render-menu');
renderMenu.addEventListener('mouseover', () => showDiv("render-buttons"));

const switcherDiv = document.getElementById('switchers');
switchers.addEventListener('mouseout', (event) => {
  if (!switcherDiv.contains(event.relatedTarget)) {
    showDiv()
  }
});
