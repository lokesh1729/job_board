import { activateCurrStep } from './controllers/step_navigation';
import { EDUCATION_DETAILS } from './controllers/constants';
import { handleAddElement, handleRemoveElement } from './controllers/form_field_events';

activateCurrStep(EDUCATION_DETAILS);
const btnMapping = JSON.parse(document.getElementById('btn_mapping').textContent);

btnMapping.forEach((item) => {
  $(`.${item.addBtnClass}`).on('click', (event) => {
    handleAddElement(event.target, item.removeBtnClass);
  });
  $(`.${item.removeBtnClass}`).on('click', (event) => {
    handleRemoveElement(event.target, item.removeBtnClass);
  });
});
