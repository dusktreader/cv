import { build as buildPlain } from "./build-plain.js";
import { build as buildFancy } from "./build-fancy.js";
import { deepUpdate, makeElement } from "./tools.js";

export var currentFormat = "fancy";

export const loadConfig = (args = {}) => {
  const queryString = window.location.search;
  const urlParams = new URLSearchParams(queryString);

  fetch("static/cv.json")
    .then(r => r.json())
    .then(data => {
      var cv = data.main;

      const role = urlParams.get("role") || "staff";
      if (role !== "staff") {
        deepUpdate(cv, data.profiles[role]);
      }

      const color = urlParams.get("color") || "light";
      const format = urlParams.get("format") || "fancy";
      const size = urlParams.get("size") || "medium";

      switch (format) {
        case "plain":
          buildPlain(cv);
          break;
        case "fancy":
          buildFancy(cv, color, size);
          break;
      }
    })
    .catch(e => {
      console.error("Error fetching json: ", e);
    });
}
