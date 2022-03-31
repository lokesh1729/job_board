const STEP1 = 0;
const STEP2 = 1;
const STEP3 = 2;
const STEP4 = 3;

let stepsMapping = {
  [STEP1]: 'education-details',
  [STEP2]: 'work-details',
  [STEP3]: 'project-details',
  [STEP4]: 'skill-details'
};

let stepsSequence = [STEP1, STEP2, STEP3, STEP4];

let currStep = STEP1;

function activateCurrStep(number) {
  const curr = stepsMapping[number];
  const ele = $(`#step-header div[data-link-to=${curr}]`);
  $(ele).addClass('activate-step');
  $(`#${curr}`).show();

  stepsSequence
    .filter((item) => item < number)
    .forEach((item) => {
      const currId = stepsMapping[item];
      $(`#${currId}`).hide();
    });

  stepsSequence
    .filter((item) => item > number)
    .forEach((item) => {
      const currId = stepsMapping[item];
      const ele = $(`#step-header div[data-link-to=${currId}]`);
      $(ele).removeClass('activate-step');
      $(`#${currId}`).hide();
    });
}

function nextStepHandler(number) {
  activateCurrStep(number);
  // hide previous steps
  $('#prev-btn').removeAttr('disabled');
  if (number === STEP4) {
    $('#next-btn').text('Submit');
  } else if (number > STEP4) {
    $('#next-btn').attr('disabled', true);
  }
}

function previousStepHandler(number) {
  activateCurrStep(number);
  $('#next-btn').removeAttr('disabled');
  if (number <= STEP1) {
    $('#prev-btn').attr('disabled', true);
  }
  if ($('#next-btn').text().trim() === 'Submit') {
    $('#next-btn').text('Next');
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
            if ($(element).find(`input[type="hidden"][name="pk"]`).toArray().length > 0) {
              $(element).append(`<input type="hidden" name="pk" value="${data.pop()}" />`);
            }
          }
        );
        if (currStep === STEP4) {
          window.location.href = '/candidate/dashboard';
        } else {
          nextStepHandler(stepsSequence[currStep + 1]);
        }
      });
      req.fail((result, status, error) => {
        console.error(`error in ajax request ${error} for url ${event.target.action}`);
        throw new Error('failed in making ajax request');
      });
    }
    form.classList.add('was-validated');
  });
  $(form).submit();
};

activateCurrStep(currStep);

$('#next-btn').on('click', function (event) {
  try {
    validateStep(currStep);
    currStep++;
  } catch (err) {
    console.error('error in clicking next button');
  }
});

$('#prev-btn').on('click', function (event) {
  previousStepHandler(stepsSequence[--currStep]);
});
