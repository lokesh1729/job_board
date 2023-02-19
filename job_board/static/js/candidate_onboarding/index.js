import { activateCurrStep } from './controllers/step_navigation';
import { handleAddElement, handleRemoveElement } from './controllers/form_field_events';

function getPaths() {
  const paths = window.location.pathname.split('/onboarding/');
  return paths.length > 1 ? paths : [];
}
const paths = getPaths();
activateCurrStep(paths[paths.length - 1]);
const btnEle = document.getElementById('btn_mapping');
if (btnEle) {
  const btnMapping = JSON.parse(btnEle.textContent);

  btnMapping.forEach((item) => {
    $(`.${item.addBtnClass}`).on('click', (event) => {
      handleAddElement(event.target, item.removeBtnClass);
    });
    $(`.${item.removeBtnClass}`).on('click', (event) => {
      handleRemoveElement(event.target, item.removeBtnClass);
    });
  });
}
const expandCollapseBtn = $('#expand-collapse-btn');
if (expandCollapseBtn) {
  // by default the filters are shown
  $('#angles-down-icon').hide();
  expandCollapseBtn.on('click', (event) => {
    if ($('#angles-up-icon').is(':visible')) {
      $('#angles-up-icon').hide();
      $('#angles-down-icon').show();
      $('#filter-form').hide();
    } else {
      $('#angles-up-icon').show();
      $('#angles-down-icon').hide();
      $('#filter-form').show();
    }
  });
}
