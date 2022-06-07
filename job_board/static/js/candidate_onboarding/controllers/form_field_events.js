/** This function updates id and for attributes of form elements
 * 
 *  1. Each form element has ".form-field" class, so iterate over it.
 *  2. Find the label element and input element.
 *  3. "for" and "id" are joined by "--". so, split it and join it back
 *       with the new sequence.
 * 
**/

const updateFormElementIds = (formElement, idx) => {
  for (const currElement of formElement.find('.form-field').toArray()) {
    const labelEle = currElement.children[0];
    const inputEle = currElement.children[1];
    const forVal = labelEle.getAttribute('for').split('--');
    labelEle.setAttribute('for', `${forVal[0]}--${idx}`);
    const idVal = inputEle.getAttribute('id').split('--');
    inputEle.setAttribute('id', `${idVal[0]}--${idx}`);
  }
};

/**
 * This function is an event handler for "Add <form type>" for the form
 *   elements
 * 
 * 1. deep-copy the wrapper element. Refer docs/candidate_onboarding.md for
 *    the context on the element structuring
 * 2. we need to change the form element ids. Why ? for every form element,
 *    there is a label element associated. We need to keep them consistent for
 *    accessibility and best practices
 *     Ref - https://developer.mozilla.org/en-US/docs/Web/HTML/Element/label
 * 3. For the cloned wrapper element which is added, increment the sequence to
 *     parent wrapper element's sequence + 1
 * 4. Also, for the elements below the parent element, update their sequences
 *     because they are changed now. ** Think of it like updating an array from
 *     the current position to the end of it. **
 * 5. Enable the remove buttons of both parent and cloned element
 * 
 * 
**/
const handleAddElement = (element, dataAttrVal, removeBtnClass) => {
  const dataAttrName = "data-group";
  const parentWrapper = $(element).parent().parent();
  const clonedEle = $(parentWrapper.clone(true));
  let seq = parseInt(parentWrapper.attr(dataAttrName).split("--")[1]);
  updateFormElementIds(clonedEle, ++seq);
  clonedEle.attr(dataAttrName, `${dataAttrVal}--${seq}`);
  for (const currSibbling of parentWrapper.nextAll().toArray()) {
    updateFormElementIds($(currSibbling), ++seq);
    $(currSibbling).attr(dataAttrName, seq);
  }
  clonedEle.insertAfter(parentWrapper);
  parentWrapper.find(removeBtnClass).removeAttr('disabled');
  clonedEle.find(removeBtnClass).removeAttr('disabled');
  clonedEle.find("input[type='hidden']").remove();
};

/** This function is an event handler for "Delete <form type>" for the form
 *   elements
 *  1. Update the sequence of sibblings of the current element to current
 *       sequence and seq+1 and so on...
 *  2. Delete the current wrapper element
 *  3. If there is only one element remaining i.e. prevSibblings + nextSibblings
 *       == 1, then disable their remove button.
**/

const handleRemoveElement = (element, dataAttrVal, removeBtnClass) => {
  const dataAttrName = "data-group";
  const parentWrapper = $(element).parent().parent();
  let seq = parseInt(parentWrapper.attr(dataAttrName).split("--")[1]);
  const nextSibblings = parentWrapper.nextAll('div[data-group]').toArray();
  const prevSibblings = parentWrapper.prevAll('div[data-group]').toArray();
  if (nextSibblings.length + prevSibblings.length == 0) {
    alert("unable to remove the element as there is only one left");
    $(element).attr('disabled', true);
    return;
  }
  parentWrapper.remove();
  for (const currSibbling of nextSibblings) {
    updateFormElementIds($(currSibbling), seq);
    $(currSibbling).attr(dataAttrName, `${dataAttrVal}--${seq++}`);
  }
  if (nextSibblings.length + prevSibblings.length === 1) {
    for (const currSibbling of nextSibblings) {
      $(currSibbling).find(removeBtnClass).attr('disabled', true);
    }
    for (const currSibbling of prevSibblings) {
      $(currSibbling).find(removeBtnClass).attr('disabled', true);
    }
  }
};

export { handleAddElement, handleRemoveElement };
