export const cap = (text) => {
  return text.charAt(0).toUpperCase() + text.slice(1);
};

export const deepUpdate = (target, source) => {
  for (const key in source) {
    if (source.hasOwnProperty(key)) {
      if (source[key] !== null && typeof source[key] === 'object' && target[key]) {
        deepUpdate(target[key], source[key]);
      } else if (source[key] !== null) {
        target[key] = source[key];
      }
    }
  }
  return target;
};

export const withDiv = (attrs, innerFunc) => {
  const div = makeElement("div", attrs);

  try {
    innerFunc(div);
  } catch(e) {
    console.error("Error while binding div: ", e);
  } finally {
    return div;
  }
};

export const makeElement = (tag, attrs) => {
  const element = document.createElement(tag);
  const { klass, html, ...rest } = attrs;
  if (klass !== undefined) {
    element.setAttribute("class", klass);
  }
  if (html !== undefined) {
    element.innerHTML = html;
  }
  Object.entries(rest).map( ([k, v]) => {
    element.setAttribute(k, v);
  });
  return element;
};

export const addKids = (parent, ...kids) => {
  kids.map((kid) => parent.appendChild(kid));
  return parent;
};

export const setUrlParams = (arg) => {
  var urlParams;
  if (!!arg.clear) {
    urlParams = new URLSearchParams();
    delete arg.clear;
  } else {
    urlParams = new URLSearchParams(window.location.search);
  }
  Object.entries(arg).forEach(([key, value]) => {
    urlParams.set(key, value);
  });
  window.location.search = urlParams
};

export const maybeUpdateCss = (id, kind, key) => {
  const url = `static/css/${kind}/${key}.css`
  const css = document.getElementById(id)
  if (css === null) {
    document.getElementsByTagName("head")[0].appendChild(
      makeElement("link", { id: id, rel: "stylesheet", type: "text/css", href: url }),
    );
  } else if (css.href !== url) {
    css.replaceWith(
      makeElement("link", { id: id, rel: "stylesheet", type: "text/css", href: url }),
    );
  }
}

