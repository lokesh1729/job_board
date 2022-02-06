const STEP1 = 1;
const STEP2 = 2;
const STEP3 = 3;
const STEP4 = 4;

let stepsMapping = {
  [STEP1]: "education-details",
  [STEP2]: "work-details",
  [STEP3]: "project-details",
  [STEP4]: "skill-details",
};

let stepsSequence = [STEP1, STEP2, STEP3, STEP4];

let currStep = 0;

function activateCurrStep(number) {
  const curr = stepsMapping[number];
  const ele = $(`#step-header div[data-link-to=${curr}]`).children()[0];
  $(ele).removeClass("tw-bg-gray-400");
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
      const ele = $(`#step-header div[data-link-to=${currId}]`).children()[0];
      $(ele).addClass("tw-bg-gray-400");
      $(`#${currId}`).hide();
    });
    $("#next-btn").removeAttr("disabled");
    if (number <= STEP1) {
        $("#prev-btn").attr("disabled", true);
    }
}

$("#next-btn").on("click", function (event) {
  event.preventDefault();
  gotoNextStep(stepsSequence[++currStep]);
});

$("#prev-btn").on("click", function (event) {
  event.preventDefault();
  gotoPreviousStep(stepsSequence[--currStep]);
});

gotoNextStep(stepsSequence[currStep]);
gotoPreviousStep(stepsSequence[currStep]);
