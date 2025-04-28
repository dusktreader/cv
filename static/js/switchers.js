import { loadConfig } from "./build.js";
import { makeElement } from "./tools.js";

const head = document.getElementsByTagName('head')[0];

const showDiv = (id) => {
  Array.from(document.getElementsByClassName("switcher-buttons")).map(e => {
    e.style.removeProperty('display');
  });

  if (id !== undefined) {
    document.getElementById(id).style.display = "flex";
  }
};


// Role Controls

Array.from(document.getElementsByClassName("role-button")).map( e => {
  e.addEventListener("click", () => changeRole(e.role));
});

export const changeRole = (key) => {
  loadConfig({ profile: key });
}

const roleMenu = document.getElementById('role-menu').addEventListener('mouseover', () => {
  showDiv("role-buttons");
});


// Color Controls

Array.from(document.getElementsByClassName("color-button")).map( e => {
  e.addEventListener("click", () => changeColor(e.getAttribute("color")));
});

export const changeColor = (key) => {
  const path = `static/css/colors/${key}.css`;
  const oldCss = document.getElementById("color-style");
  if (oldCss.getAttribute("href") !== path) {
    oldCss.replaceWith(makeElement(
      "link",
      { id: "color-style", rel: "stylesheet", type: "text/css", href: path }
    ));
  }
}

const colorMenu = document.getElementById('color-menu').addEventListener('mouseover', () => {
  showDiv("color-buttons");
});


// Size Controls

Array.from(document.getElementsByClassName("size-button")).map( e => {
  e.addEventListener("click", () => changeSize(e.getAttribute("size")));
});

export const changeSize = (key) => {
  const path = `static/css/sizes/${key}.css`;
  const oldCss = document.getElementById("size-style");
  if (oldCss.getAttribute("href") !== path) {
    oldCss.replaceWith(makeElement(
      "link",
      { id: "size-style", rel: "stylesheet", type: "text/css", href: path }
    ));
  }
}

const sizeMenu = document.getElementById('size-menu').addEventListener('mouseover', () => {
  showDiv("size-buttons");
});


// Render Controls

Array.from(document.getElementsByClassName("render-button")).map( e => {
  e.addEventListener("click", () => render(e.format));
});

export const render = (format) => {
  window.print();
}

const renderMenu = document.getElementById('render-menu').addEventListener('mouseover', () => {
  showDiv("render-buttons")
});


// Format Controls

Array.from(document.getElementsByClassName("format-button")).map( e => {
  e.addEventListener("click", () => loadConfig({ format: e.getAttribute("format") }));
});

const formatMenu = document.getElementById('format-menu').addEventListener('mouseover', () => {
  showDiv("format-buttons")
});




const switcherDiv = document.getElementById('switchers');
switchers.addEventListener('mouseout', (event) => {
  if (!switcherDiv.contains(event.relatedTarget)) {
    showDiv()
  }
});
