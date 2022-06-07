import { stepsMapping } from  "./controllers/constants";
import { formHandler, activateCurrStep } from "./controllers/step_navigation";
import { handleAddElement, handleRemoveElement } from "./controllers/form_field_events";
import { eventMap, STEP1, STEP4 } from "./controllers/constants";

for (let key in stepsMapping) {
    $(`#${stepsMapping[key]}`).on('submit', formHandler);
}

$('.next-btn').on('click', function (event) {
  event.stopPropagation();
  let currStep = parseInt(event.target.getAttribute("data-step-number"));
  console.log("currStep in next button is " + currStep);
  try {
    const currForm = stepsMapping[currStep];
    if (!currForm) {
      console.error("invalid currStep");
      return;
    }
    $(`#${currForm}`).submit();
    setTimeout(() => {
      if (currStep === STEP4) {
        window.location.href = '/candidate/dashboard';
      } else {
        activateCurrStep(currStep + 1);
      }
    }, 500);
  } catch (err) {
    console.error('error in clicking next button', err);
  }
});

/**
* When a previous button is clicked, there is no need of
* validating the current step. Why ?
*
* User may not filled the current step completely but he may want to
* go to the previous step to verify some of the information.
**/

$('.prev-btn').on('click', function (event) {
  event.stopPropagation();
  let currStep = parseInt(event.target.getAttribute("data-step-number"));
  console.log("currStep in previous button is " + currStep);
  activateCurrStep(currStep - 1);
});

activateCurrStep(STEP1);

eventMap.forEach((item) => {
  $(item.addBtnClass).on('click', (event) => {
    handleAddElement(event.target, item.dataAttrVal, item.removeBtnClass);
  });
  $(item.removeBtnClass).on('click', (event) => {
    handleRemoveElement(event.target, item.dataAttrVal, item.removeBtnClass);
  });
});

