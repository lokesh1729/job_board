/*
* This file contains event handlers for "Previous" and "Next"
* buttons for the steps
*/
import { stepsMapping, stepsSequence, STEP1, STEP4 } from "./constants";

/**
 * When clicked on Prev/Next button in the candidate onboarding page,
 * This function is responsible to display that step.
 *
 * How to display the step ?
 *
 * Refer `docs/candidate_onboarding.md` for the context
 *
 * 1. Activate the step in the step header.
 * 2. Activate the current step in the step form.
 *      a. Hide all the steps less than the given `number`
 *      b. Hide all the steps greater than the given `number` and
 *          also deactivate in the header
 *      We shouldn't deactivate the header for steps less than given `number`
 *      Why ? because, when user done with a step, we need to keep showing,
 *      it is already done whereas the other steps we shouldn't show activated.
 * 3. Activate prev and next buttons (just in case if they are disabled before)
 *    The edge cases are self-explanatory.
 *
**/
function activateCurrStep(number) {
  console.log("activating currStep " + number);
  const form = stepsMapping[number];
  const ele = $(`#step-header div[data-link-to=${form}]`);
  $(ele).addClass('activate-step');
  $(`#${form}`).addClass("needs-validation");
  $(`#${form}`).removeClass("was-validated");
  $(`#${form}`).parent().show();

  stepsSequence
    .filter((item) => item < number)
    .forEach((item) => {
      const currForm = stepsMapping[item];
      $(`#${currForm}`).parent().hide();
    });

  stepsSequence
    .filter((item) => item > number)
    .forEach((item) => {
      const currForm = stepsMapping[item];
      const ele = $(`#step-header div[data-link-to=${currForm}]`);
      $(ele).removeClass('activate-step');
      $(`#${currForm}`).parent().hide();
    });

    const prevBtn = $(`#${form} + div > .prev-btn`);
    const nextBtn = $(`#${form} + div > .next-btn`);

    $(prevBtn).removeAttr('disabled');
    $(nextBtn).removeAttr('disabled');

    if (number <= STEP1) {
      $(prevBtn).attr('disabled', true);
    } else if (number === STEP4) {
      $(nextBtn).text('Submit');
    } else if (number > STEP4) {
      $(nextBtn).attr('disabled', true);
    } else if (number < STEP4 && $(nextBtn).text().trim() === 'Submit') {
      $(nextBtn).text('Next');
    }
}

function formHandler (event) {
  event.preventDefault();
  event.stopPropagation();
  const form = event.target;
  form.classList.remove('needs-validation');
  form.classList.add('was-validated');
  if (!form.checkValidity()) {
    throw new Error("form validation failed");
  }
  let data = [];
  const stepName = form.getAttribute('id');
  const formName = form.getAttribute('name');
  Array.from(form.getElementsByClassName(`${stepName}--wrapper`)).forEach((element) =>
    data.push(
      $(element)
        .find('input, select, textarea')
        .toArray()
        .reduce(
          (acc, curr) =>
            Object.assign(acc, {
              [curr.name]: curr.value
            }),
          {}
        )
    )
  );
  const req = $.ajax(form.action, {
    accepts: 'application/json',
    contentType: 'application/json',
    method: form.method,
    headers: {
      'X-CSRFToken': $(form).find("input[name='csrfmiddlewaretoken']").attr('value')
    },
    data: JSON.stringify({
      data: data,
      form_type: formName
    })
  });
  req.done((result, status, jqXHR) => {
    let data = result.result;
    data.reverse();
    Array.from(form.getElementsByClassName(`${stepName}--wrapper`)).forEach(
      (element) => {
        if ($(element).find('input[type="hidden"][name="pk"]').toArray().length > 0) {
          $(element).find('input[type="hidden"][name="pk"]').attr("value", `${data.pop()}`);
        } else {
          $(element).append(`<input type="hidden" name="pk" value="${data.pop()}" />`);
        }
      }
    );
  });
  req.fail((result, status, error) => {
    console.error(`error in ajax request ${error} for url ${form.action}`);
    throw new Error('failed in making ajax request');
  });
}

for (let key in stepsMapping) {
    $(`#${stepsMapping[key]}`).on('submit', formHandler);
}
/**
* When a next button is clicked, we should take the user
* to the next step but before that we need to validate
*
*
* It first validates the current step, make an AJAX call to save
* the current state, then moves to the next step.
*
* 1. `event.target` is the form element here because the event handler is
*     running on the submit of form.
* 2. Loop through all form wrapper elements and get the values of input
*     elements and push it to `data` array.
* 3. The result of the API would be an array of the objects contains
*     "pk" of an object. Put them inside the wrapper element as hidden element.
*
**/
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
