/** This function updates id and for attributes of form elements
 *
 *  1. Iterate over form elements
 *  2. Split them by regex
 *  3. Update them by adding index
 *
 **/

const updateFormElementIds = (formElement, idx) => {
  for (const currElement of formElement.find('input,select,textarea').toArray()) {
    const sibbling = $(currElement).siblings('label').toArray()[0];
    const parent = $(currElement).parent('div').toArray()[0];
    const regex = /^([a-zA-Z_-]*)[0-9]+([a-zA-Z_-]*)$/;
    try {
      $(currElement).attr('id', $(currElement).attr('id').match(regex).slice(1).join(idx));
      $(currElement).attr('name', $(currElement).attr('name').match(regex).slice(1).join(idx));
      $(sibbling).attr('for', $(sibbling).attr('for').match(regex).slice(1).join(idx));
      $(parent).attr('id', $(parent).attr('id').match(regex).slice(1).join(idx));
    } catch (e) {
      console.error(e);
    }
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
const handleAddElement = (element, removeBtnClass) => {
  const dataAttrName = 'data-form-index';
  const parentWrapper = $(element).parent().parent();
  const clonedEle = $(parentWrapper.clone(true));
  let seq = parseInt(parentWrapper.attr(dataAttrName));
  updateFormElementIds(clonedEle, ++seq);
  clonedEle.attr(dataAttrName, seq);
  for (const currSibbling of parentWrapper.nextAll().toArray()) {
    updateFormElementIds($(currSibbling), ++seq);
    $(currSibbling).attr(dataAttrName, seq);
  }
  clonedEle.insertAfter(parentWrapper);
  clonedEle.find('input[type="hidden"]').remove();
  parentWrapper.find(removeBtnClass).removeAttr('disabled');
  clonedEle.find(removeBtnClass).removeAttr('disabled');
  $('#id_form-TOTAL_FORMS').attr(
    'value',
    parseInt($('#id_form-TOTAL_FORMS').attr('value'), 10) + 1
  );
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
  const dataAttrName = 'data-form-index';
  const parentWrapper = $(element).parent().parent();
  let seq = parseInt(parentWrapper.attr(dataAttrName));
  const nextSibblings = parentWrapper.nextAll(`div[${dataAttrName}]`).toArray();
  const prevSibblings = parentWrapper.prevAll(`div[${dataAttrName}]`).toArray();
  if (nextSibblings.length + prevSibblings.length == 0) {
    alert('unable to remove the element as there is only one left');
    $(element).attr('disabled', true);
    return;
  }
  parentWrapper.remove();
  for (const currSibbling of nextSibblings) {
    updateFormElementIds($(currSibbling), seq);
    $(currSibbling).attr(dataAttrName, seq);
    seq++;
  }
  if (nextSibblings.length + prevSibblings.length === 1) {
    for (const currSibbling of nextSibblings) {
      $(currSibbling).find(removeBtnClass).attr('disabled', true);
    }
    for (const currSibbling of prevSibblings) {
      $(currSibbling).find(removeBtnClass).attr('disabled', true);
    }
  }
  $('#id_form-TOTAL_FORMS').attr(
    'value',
    parseInt($('#id_form-TOTAL_FORMS').attr('value'), 10) - 1
  );
};

export { handleAddElement, handleRemoveElement };
