import { stepsMapping, stepsSequence } from "./form_state.js";


const validateStep = function (currStep) {
	const curr = stepsMapping[stepsSequence[currStep]];
	const form = document.getElementById(`${curr}`);
	let isValid = true;
	$(form).submit(function (event) {
		if (!form.checkValidity()) {
		  isValid = false;
          event.preventDefault();
          event.stopPropagation();
        }
        form.classList.add('was-validated');
	});
	$(form).submit();
	return isValid;
}

export { validateStep };