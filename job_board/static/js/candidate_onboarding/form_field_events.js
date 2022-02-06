const updateFormElementIds = (formElement, idx) => {
  for (const currElement of formElement.find(".form-field").toArray()) {
    const labelEle = currElement.children[0];
    const inputEle = currElement.children[1];
    const forVal = labelEle.getAttribute("for").split("__");
    labelEle.setAttribute("for", `${forVal[0]}__${idx}`);
    const idVal = inputEle.getAttribute("id").split("__");
    inputEle.setAttribute("id", `${idVal[0]}__${idx}`);
  }
};

const handleAddElement = (element, dataAttrName, removeBtnClass) => {
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
  // enable remove element for current and next element
  $(wrapperElement).find(removeBtnClass).removeAttr("disabled");
  $(clonedEle).find(removeBtnClass).removeAttr("disabled");
};

const handleRemoveElement = (element, dataAttrName, removeBtnClass) => {
  const wrapperElement = $(element).parent().parent();
  let seq = parseInt(wrapperElement.get(0).getAttribute(dataAttrName));
  const nextSibblings = wrapperElement.nextAll().toArray();
  const prevSibblings = wrapperElement.prevAll().toArray();
  $(wrapperElement).remove();
  for (const currSibbling of nextSibblings) {
    updateFormElementIds($(currSibbling), seq);
    $(currSibbling).attr(dataAttrName, seq++);
  }
  if (nextSibblings.length + prevSibblings.length === 1) {
    for (const currSibbling of nextSibblings) {
      $(currSibbling).find(removeBtnClass).attr("disabled", true);
    }
    for (const currSibbling of prevSibblings) {
      $(currSibbling).find(removeBtnClass).attr("disabled", true);
    }
  }
};

let eventMap = [
  {
    addBtnClass: ".add-education",
    dataAttrName: "data-edu-id",
    removeBtnClass: ".remove-education",
  },
  {
    addBtnClass: ".add-work",
    dataAttrName: "data-work-id",
    removeBtnClass: ".remove-work",
  },
  {
    addBtnClass: ".add-project",
    dataAttrName: "data-project-id",
    removeBtnClass: ".remove-project",
  },
  {
    addBtnClass: ".add-skill",
    dataAttrName: "data-skill-id",
    removeBtnClass: ".remove-skill",
  },
];

eventMap.forEach((item) => {
  $(item.addBtnClass).on("click", (event) => {
    const element = $(event.target);
    handleAddElement(element, item.dataAttrName, item.removeBtnClass);
  });
  $(item.removeBtnClass).on("click", (event) => {
    const element = $(event.target);
    handleRemoveElement(element, item.dataAttrName, item.removeBtnClass);
  });
});
