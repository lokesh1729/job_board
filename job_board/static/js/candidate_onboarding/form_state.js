const STEP1 = 1;
const STEP2 = 2;
const STEP3 = 3;
const STEP4 = 4;

let stepsMapping = {
  [STEP1]: "education-details",
  [STEP2]: "work-details",
  [STEP3]: "project-details",
  [STEP4]: "skill-details",
};


let stepsSequence = [STEP1, STEP2, STEP3, STEP4];

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

export {stepsMapping, stepsSequence, eventMap, STEP1, STEP2, STEP3, STEP4};