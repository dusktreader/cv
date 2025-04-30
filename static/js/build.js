import { build as buildPlain } from "./build-plain.js";
import { build as buildFancy } from "./build-fancy.js";
import { deepUpdate } from "./tools.js";

export var currentFormat = "fancy";
export var currentProfile = "staff";

export const loadConfig = (args = {}) => {
  fetch("static/cv.json")
    .then(r => r.json())
    .then(data => {
      var cv = data.main;

      if (args.profile !== undefined && args.profile !== currentProfile) {
        deepUpdate(cv, data.profiles[args.profile]);
        currentProfile = args.profile;
      }

      var format = currentFormat
      if (args.format !== undefined) {
        format = args.format;
      }
      buildPage(cv, format);
    })
    .catch(e => {
      console.error("Error fetching json: ", e);
    });
}

const buildPage = (data, format) => {
  switch (format) {
    case "plain":
      buildPlain(data);
      break;
    case "fancy":
      buildFancy(data);
      break;
  }
  currentFormat = format;
}
