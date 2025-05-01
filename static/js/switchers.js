import { loadConfig } from "./build.js";
import { makeElement, setUrlParams } from "./tools.js";

const head = document.getElementsByTagName('head')[0];

const hideButtons = () => {
  Array.from(document.getElementsByClassName("switcher-buttons")).map(e => {
    e.style.display = "none";
  });
};


const showButtons = (id) => {
  hideButtons()
  if (id !== undefined) {
    document.getElementById(id).style.display = "flex";
  }
};


// Main menu

const mainMenu = document.getElementById('main-menu');
const subMenu = document.getElementById("sub-menu")
mainMenu.addEventListener('mouseover', () => {
  mainMenu.style.display = "none";
  subMenu.style.display = "flex";
});

const switcherDiv = document.getElementById('switchers');
switcherDiv.addEventListener('mouseout', (event) => {
  if (!switcherDiv.contains(event.relatedTarget)) {
    hideButtons()
    mainMenu.style.display = "flex";
    subMenu.style.display = "none";
  }
});


// Role Controls

Array.from(document.getElementsByClassName("role-button")).map( e => {
  e.addEventListener("click", () => setUrlParams({ role: e.getAttribute("role") }));
});

const roleMenu = document.getElementById('role-menu').addEventListener('mouseover', () => {
  showButtons("role-buttons");
});


// Color Controls

Array.from(document.getElementsByClassName("color-button")).map( e => {
  e.addEventListener("click", () => setUrlParams({ color: e.getAttribute("color") }));
});

const colorMenu = document.getElementById('color-menu').addEventListener('mouseover', () => {
  showButtons("color-buttons");
});


// Size Controls

Array.from(document.getElementsByClassName("size-button")).map( e => {
  e.addEventListener("click", () => setUrlParams({ size: e.getAttribute("size") }));
});

const sizeMenu = document.getElementById('size-menu').addEventListener('mouseover', () => {
  showButtons("size-buttons");
});


// Render Controls

Array.from(document.getElementsByClassName("render-button")).map( e => {
  e.addEventListener("click", () => window.print());
});

const renderMenu = document.getElementById('render-menu').addEventListener('mouseover', () => {
  showButtons("render-buttons")
});


// Format Controls

Array.from(document.getElementsByClassName("format-button")).map( e => {
  e.addEventListener("click", () => setUrlParams({ format: e.getAttribute("format"), clear: true }));
});

const formatMenu = document.getElementById('format-menu').addEventListener('mouseover', () => {
  showButtons("format-buttons")
});
