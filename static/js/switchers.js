const head = document.getElementsByTagName('head')[0];

const changeColor = (color) => {
  console.log("Chosen theme: ", color);
  var colorStyle = document.getElementById('color-style');
  colorStyle.remove();

  const colorPath = `static/css/${color}.css`;

  colorStyle = document.createElement('link');
  colorStyle.setAttribute('rel', 'stylesheet');
  colorStyle.setAttribute('type', 'text/css');
  colorStyle.setAttribute('id', 'color-style');
  colorStyle.setAttribute('href', colorPath);
  head.appendChild(colorStyle);
};

const changeSize = (size) => {
  console.log("Chosen size: ", size);
  var sizeStyle = document.getElementById('size-style');
  sizeStyle.remove();

  const sizePath = `static/css/${size}.css`;

  sizeStyle = document.createElement('link');
  sizeStyle.setAttribute('rel', 'stylesheet');
  sizeStyle.setAttribute('type', 'text/css');
  sizeStyle.setAttribute('id', 'size-style');
  sizeStyle.setAttribute('href', sizePath);
  head.appendChild(sizeStyle);
};

const showDiv = (id) => {

  Array.from(document.getElementsByClassName("switcher-buttons")).map(e => {
    e.style.removeProperty('display');
  });

  if (id !== undefined) {
    document.getElementById(id).style.display = "flex";
  }
};

const colorMenu = document.getElementById('color-menu');
colorMenu.addEventListener('mouseover', () => showDiv("color-buttons"));

const sizeMenu = document.getElementById('size-menu');
sizeMenu.addEventListener('mouseover', () => showDiv("size-buttons"));

const downloadMenu = document.getElementById('download-menu');
downloadMenu.addEventListener('mouseover', () => showDiv("download-buttons"));

const switcherDiv = document.getElementById('switchers');
switchers.addEventListener('mouseout', (event) => {
  if (!switcherDiv.contains(event.relatedTarget)) {
    showDiv()
  }
});
