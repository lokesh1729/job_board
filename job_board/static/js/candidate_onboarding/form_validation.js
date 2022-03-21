import { stepsMapping, stepsSequence } from "./form_state.js";

const validateStep = function (currStep) {
	const curr = stepsMapping[stepsSequence[currStep]];
	const form = document.getElementById(`${curr}`);
	let isValid = true;
	$(form).submit(function (event) {
		event.preventDefault();
		event.stopPropagation();
		if (!form.checkValidity()) {
			isValid = false;
		} else {
			let data = [];
			const stepName = event.target.getAttribute("id");
			Array.from(
				event.target.getElementsByClassName(`${stepName}--wrapper`)
			).forEach((element) =>
				data.push(
					$(element)
						.find("input")
						.toArray()
						.reduce(
							(acc, curr) =>
								Object.assign(acc, {
									[curr.name]: curr.value,
								}),
							{}
						)
				)
			);
			$.ajax(event.target.action, {
				method: event.target.method,
				headers: {
					"X-CSRFToken": $(event.target)
						.find("input[name='csrfmiddlewaretoken']")
						.attr("value"),
				},
				data: {
					data: data,
				},
				complete: (result, status) => {
					console.log(`ajax request status ${status}`);
					console.log(
						`ajax request success ${JSON.stringify(result)}`
					);
				},
				error: (result, status, error) => {
					console.error(
						`error in ajax request ${error} for url ${event.target.action}`
					);
				},
			});
		}
		form.classList.add("was-validated");
	});
	$(form).submit();
	return isValid;
};

export { validateStep };
