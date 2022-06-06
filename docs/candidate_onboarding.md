### Candidate Onboarding

1. This page has 3 parts. One is step header, Second is steps, Third is prev and next buttons. All three are wrapped in a flex container with column orientation. Refer to `templates/candidate/onboarding/main.html`.
2. Each header has `element.data_link_to` which should be linked to the `form.id` attribute of
	each step i.e. the symantic links are defined in such a way.
2. There is a form for each step. The id would be `step_header_mapping.0.data_link_to` and name would be `step_header_mapping.0.name`. These mappings are defined in `candidate/constants.py` --> `OnboardingSteps` class.
3. Inside the form,
    1. There is a div at the level 0 (root) with "data-" tag. For example, "data-edu-id"
    2. At level 1, there is another div which is called "wrapper" div. For example, "education-details--wrapper"
    3. At level 2, there will be form elements defined at each row. For example, in the first row two input elements, in the second row two date inputs etc...
    4. At level 1 (sibbling to the wrapper), there are two buttons to add/remove new form rows.