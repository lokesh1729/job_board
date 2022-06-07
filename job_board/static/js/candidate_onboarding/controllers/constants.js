const STEP1 = 1;
const STEP2 = 2;
const STEP3 = 3;
const STEP4 = 4;

const EDUCATION_DETAILS = "education-details";
const WORK_DETAILS = "work-details";
const PROJECT_DETAILS = "project-details";
const SKILL_DETAILS = "skill-details";

let stepsMapping = {
  [STEP1]: EDUCATION_DETAILS,
  [STEP2]: WORK_DETAILS,
  [STEP3]: PROJECT_DETAILS,
  [STEP4]: SKILL_DETAILS
};

let stepsSequence = [STEP1, STEP2, STEP3, STEP4];

let eventMap = [
  {
    addBtnClass: '.add-education',
    removeBtnClass: '.remove-education',
    dataAttrVal: EDUCATION_DETAILS,
  },
  {
    addBtnClass: '.add-work',
    removeBtnClass: '.remove-work',
    dataAttrVal: WORK_DETAILS,
  },
  {
    addBtnClass: '.add-project',
    removeBtnClass: '.remove-project',
    dataAttrVal: PROJECT_DETAILS
  },
  {
    addBtnClass: '.add-skill',
    removeBtnClass: '.remove-skill',
    dataAttrVal: SKILL_DETAILS
  }
];

export { stepsMapping, stepsSequence, eventMap, STEP1, STEP4 };
