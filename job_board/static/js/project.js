// /* Project specific Javascript goes here. */
import "../../../node_modules/jquery/dist/jquery";
import "../../../node_modules/@popperjs/core/dist/umd/popper.js";
import "../../../node_modules/bootstrap/dist/js/bootstrap.js";
import "../../../node_modules/bootstrap-datepicker/dist/js/bootstrap-datepicker";

const updateFormElementIds = (formElement, idx) => {
    for (const currElement of formElement.find(".form-field").toArray()) {
      const labelEle = currElement.children[0];
      const inputEle = currElement.children[1];
      const forVal = labelEle.getAttribute("for").split("__");
      labelEle.setAttribute("for", `${forVal[0]}__${idx}`);
      const idVal = inputEle.getAttribute("id").split("__");
      inputEle.setAttribute("id", `${idVal[0]}__${idx}`);
    }
}

const handleAddElement = (element, dataAttrName) => {
  const wrapperElement = $(element).parent().parent();
  const clonedEle = $(wrapperElement).clone(true);
  // change attributes of the cloned element
  let seq = parseInt(wrapperElement.get(0).getAttribute(dataAttrName));
  updateFormElementIds(clonedEle, ++seq);
  clonedEle.attr(dataAttrName, seq);
  // change attributes of the sibblings
  for (const currSibbling of wrapperElement.nextAll().toArray()) {
    updateFormElementIds($(currSibbling), ++seq);
    $(currSibbling).attr(dataAttrName, seq);
  }
  $(clonedEle).insertAfter(wrapperElement);
}

const handleRemoveElement = (element, dataAttrName) => {
  const wrapperElement = $(element).parent().parent();
  let seq = parseInt(wrapperElement.get(0).getAttribute(dataAttrName));
  const sibblings = wrapperElement.nextAll().toArray();
  $(wrapperElement).remove();
  for (const currSibbling of sibblings) {
    updateFormElementIds($(currSibbling), seq);
    $(currSibbling).attr(dataAttrName, seq++);
  }
}


$(".add-education").on("click", (event) => {
    const element = $(event.target);
    handleAddElement(element, "data-edu-id");
});

$(".add-work").on("click", (event) => {
  const element = $(event.target);
  handleAddElement(element, "data-work-id");
});

$(".remove-education").on("click", (event) => {
  const element = $(event.target);
  handleRemoveElement(element, "data-edu-id");
});

$(".remove-work").on("click", (event) => {
  const element = $(event.target);
  handleRemoveElement(element, "data-work-id");
});