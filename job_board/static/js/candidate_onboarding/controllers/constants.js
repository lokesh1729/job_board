const ele = document.getElementById('step_header_sequence');
let stepsSequence = null;
if (ele) {
  const content = document.getElementById('step_header_sequence').textContent;
  if (content) {
    stepsSequence = JSON.parse(content);
  }
}

export { stepsSequence };
