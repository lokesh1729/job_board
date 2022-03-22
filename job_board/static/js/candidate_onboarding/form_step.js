import { STEP1, STEP2, STEP3, STEP4, stepsMapping, stepsSequence } from './form_state.js';

let currStep = 0;

function activateCurrStep(number) {
  const curr = stepsMapping[number];
  const ele = $(`#step-header div[data-link-to=${curr}]`);
  $(ele).addClass('activate-step');
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
  $('#prev-btn').removeAttr('disabled');
  if (number >= STEP4) {
    $('#next-btn').attr('disabled', true);
  }
}

function gotoPreviousStep(number) {
  activateCurrStep(number);
  stepsSequence
    .filter((item) => item > number)
    .forEach((item) => {
      const currId = stepsMapping[item];
      const ele = $(`#step-header div[data-link-to=${currId}]`);
      $(ele).removeClass('activate-step');
      $(`#${currId}`).hide();
    });
  $('#next-btn').removeAttr('disabled');
  if (number <= STEP1) {
    $('#prev-btn').attr('disabled', true);
  }
}

const validateStep = function (currStep) {
  const curr = stepsMapping[stepsSequence[currStep]];
  const form = document.getElementById(`${curr}`);
  $(form).submit(function (event) {
    event.preventDefault();
    event.stopPropagation();
    if (form.checkValidity()) {
      let data = [];
      const stepName = event.target.getAttribute('id');
      const formName = event.target.getAttribute('name');
      Array.from(event.target.getElementsByClassName(`${stepName}--wrapper`)).forEach((element) =>
        data.push(
          $(element)
            .find('input')
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
      const req = $.ajax(event.target.action, {
        accepts: 'application/json',
        contentType: 'application/json',
        method: event.target.method,
        headers: {
          'X-CSRFToken': $(event.target).find("input[name='csrfmiddlewaretoken']").attr('value')
        },
        data: JSON.stringify({
          data: data,
          form_type: formName
        })
      });
      req.done((result, status, jqXHR) => {
        let data = result.result;
        data.reverse();
        console.log(`ajax request status ${status}`);
        console.log(`ajax request success ${JSON.stringify(result)}`);
        Array.from(event.target.getElementsByClassName(`${stepName}--wrapper`)).forEach(
          (element) => {
            $(element).append(`<input type="hidden" name="pk" value="${data.pop()}" />`);
          }
        );
        gotoNextStep(stepsSequence[currStep + 1]);
      });
      req.fail((result, status, error) => {
        console.error(`error in ajax request ${error} for url ${event.target.action}`);
      });
    }
    form.classList.add('was-validated');
  });
  $(form).submit();
};

gotoNextStep(stepsSequence[currStep]);
gotoPreviousStep(stepsSequence[currStep]);

$('#next-btn').on('click', function (event) {
  validateStep(currStep);
  currStep++;
});

$('#prev-btn').on('click', function (event) {
  debugger;
  gotoPreviousStep(stepsSequence[--currStep]);
});
