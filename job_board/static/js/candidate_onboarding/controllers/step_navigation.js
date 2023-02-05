/*
 * This file contains event handlers for "Previous" and "Next"
 * buttons for the steps
 */
import { stepsSequence } from './constants';

/**
 * When clicked on Prev/Next button in the candidate onboarding page,
 * This function is responsible to display that step.
 *
 * How to display the step ?
 *
 * Refer `docs/candidate_onboarding.md` for the context
 *
 * 1. Activate the step in the step header by adding activate-step class.
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
function activateCurrStep(stepName) {
  console.log('activating currStep ' + stepName);
  const ele = $(`#step-header div[data-link-to=${stepName}]`);
  $(`#${stepName}`).addClass('needs-validation');
  $(`#${stepName}`).removeClass('was-validated');
  $(`#${stepName}`).parent().show();

  const currIdx = stepsSequence.indexOf(stepName);

  stepsSequence.forEach((item, idx) => {
    if (idx != currIdx) {
      $(`#${item}`).parent().hide();
    }
    if (idx <= currIdx) {
      $(`#step-header div[data-link-to=${item}]`).addClass('activate-step');
    }
    if (idx > currIdx) {
      $(`#step-header div[data-link-to=${item}]`).removeClass('activate-step');
    }
  });

  const prevBtn = $(`#${stepName} + div > .prev-btn`);
  const nextBtn = $(`#${stepName} + div > .next-btn`);

  $(prevBtn).removeAttr('disabled');
  $(nextBtn).removeAttr('disabled');
}

/*
 * When a next button is clicked, we should take the user
 * to the next step but before that we need to validate the form.
 *
 * 1. validate the current form. `event.target` is the form element
 *    because the event handler is running on the submit of form.
 * 2. Loop through all form wrapper elements and get the values of input
 *     elements and push it to `data` array.
 * 3. make an AJAX call to save the data.
 * 4. The result of the API would be an array of the objects contains
 *     "pk" of an object. Put them inside the wrapper element as hidden element.
 *
 */

function formHandler(event) {
  event.preventDefault();
  event.stopPropagation();
  const form = event.target;
  form.classList.remove('needs-validation');
  form.classList.add('was-validated');
  if (!form.checkValidity()) {
    throw new Error('form validation failed');
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
    Array.from(form.getElementsByClassName(`${stepName}--wrapper`)).forEach((element) => {
      if ($(element).find('input[type="hidden"][name="pk"]').toArray().length > 0) {
        $(element).find('input[type="hidden"][name="pk"]').attr('value', `${data.pop()}`);
      } else {
        $(element).append(`<input type="hidden" name="pk" value="${data.pop()}" />`);
      }
    });
  });
  req.fail((result, status, error) => {
    console.error(`error in ajax request ${error} for url ${form.action}`);
    throw new Error('failed in making ajax request');
  });
}

export { formHandler, activateCurrStep };
