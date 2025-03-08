const head = document.getElementsByTagName('head')[0];

const changeTheme = (theme) => {
  console.log("Chosen theme: ", theme);
  var colorStyle = document.getElementById('color-style');
  colorStyle.remove();


  const colorPath = `static/css/${theme}.css`;

  colorStyle = document.createElement('link');
  colorStyle.setAttribute('rel', 'stylesheet');
  colorStyle.setAttribute('type', 'text/css');
  colorStyle.setAttribute('id', 'color-style');
  colorStyle.setAttribute('href', colorPath);
  head.appendChild(colorStyle);
};
