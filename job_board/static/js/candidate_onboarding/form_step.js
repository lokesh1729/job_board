import { validateStep } from "./form_validation.js";
import {
  STEP1,
  STEP2,
  STEP3,
  STEP4,
  stepsMapping,
  stepsSequence,
} from "./form_state.js";

let currStep = 0;

function activateCurrStep(number) {
  const curr = stepsMapping[number];
  const ele = $(`#step-header div[data-link-to=${curr}]`);
  $(ele).addClass("activate-step");
  $(`#${curr}`).show();
}

function gotoNextStep(number) {
  activateCurrStep(number);
  // hide previous steps
  stepsSequence
    .filter((item) => item < number)
    .forEach((item) => {
      const currId = stepsMapping[item];
      $(`#${currId}`).hide();
    });
  $("#prev-btn").removeAttr("disabled");
  if (number >= STEP4) {
    $("#next-btn").attr("disabled", true);
  }
}

function gotoPreviousStep(number) {
  activateCurrStep(number);
  stepsSequence
    .filter((item) => item > number)
    .forEach((item) => {
      const currId = stepsMapping[item];
      // const ele = $(`#step-header div[data-link-to=${currId}]`).children()[0];
      const ele = $(`#step-header div[data-link-to=${currId}]`);
      $(ele).removeClass("activate-step");
      $(`#${currId}`).hide();
    });
  $("#next-btn").removeAttr("disabled");
  if (number <= STEP1) {
    $("#prev-btn").attr("disabled", true);
  }
}

gotoNextStep(stepsSequence[currStep]);
gotoPreviousStep(stepsSequence[currStep]);

$("#next-btn").on("click", function (event) {
  const isValid = validateStep(currStep);
  if (!isValid) {
    return;
  }
  gotoNextStep(stepsSequence[++currStep]);
});

$("#prev-btn").on("click", function (event) {
  gotoPreviousStep(stepsSequence[--currStep]);
});
