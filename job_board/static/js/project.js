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


$(".add-education").on("click", (event) => {
    // clone the element first
    const element = $(event.target);
    const wrapperElement = $(element).parent().parent();
    const clonedEle = $(wrapperElement).clone(true);
    // change attributes of the cloned element
    let seq = parseInt(wrapperElement.get(0).getAttribute("data-edu-id"));
    updateFormElementIds(clonedEle, ++seq);
    clonedEle.attr("data-edu-id", seq);
    // change attributes of the sibblings
    for (const currSibbling of wrapperElement.nextAll().toArray()) {
      updateFormElementIds($(currSibbling), ++seq);
      $(currSibbling).attr("data-edu-id", seq);
    }
    $(clonedEle).insertAfter(wrapperElement);
});
