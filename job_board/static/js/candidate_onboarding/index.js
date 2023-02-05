import { activateCurrStep } from './controllers/step_navigation';
import { handleAddElement, handleRemoveElement } from './controllers/form_field_events';

const paths = window.location.pathname.split('/');
activateCurrStep(paths[paths.length - 1]);
const btnMapping = JSON.parse(document.getElementById('btn_mapping').textContent);

btnMapping.forEach((item) => {
  $(`.${item.addBtnClass}`).on('click', (event) => {
    handleAddElement(event.target, item.removeBtnClass);
  });
  $(`.${item.removeBtnClass}`).on('click', (event) => {
    handleRemoveElement(event.target, item.removeBtnClass);
  });
});
