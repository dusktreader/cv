export const cap = (text) => {
  return text.charAt(0).toUpperCase() + text.slice(1);
}

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
}

export const withDiv = (attrs, innerFunc) => {
  const div = makeElement("div", attrs);

  try {
    innerFunc(div);
  } catch(e) {
    console.error("Error while binding div: ", e);
  } finally {
    return div;
  }
}

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
}

export const addKids = (parent, ...kids) => {
  kids.map((kid) => parent.appendChild(kid));
  return parent;
}
