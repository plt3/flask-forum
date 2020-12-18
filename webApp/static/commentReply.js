function postReply() {
  const commentText = event.target.parentElement.nextElementSibling;

  if (commentText.firstElementChild !== null) {
    return;
  }

  const fullText = event.target.parentElement.innerHTML;
  const replyTo = fullText.slice(0, fullText.indexOf(' — '));

  // pleaseeeeeee refactor and despaghettify

  const form = document.createElement('form');
  form.setAttribute('action', '');
  form.setAttribute('method', 'POST');
  form.setAttribute('class', 'border rounded mt-2 p-2')

  const nameInput = document.createElement('input');
  nameInput.setAttribute('type', 'text');
  nameInput.setAttribute('name', 'username');
  nameInput.setAttribute('id', 'username');
  nameInput.setAttribute('placeholder', 'username');
  nameInput.className = 'form-control mb-2';
  nameInput.required = true;

  const contentInput = document.createElement('textarea');
  contentInput.setAttribute('name', 'content');
  contentInput.setAttribute('id', 'content');
  contentInput.setAttribute('placeholder', `Reply to ${replyTo}...`);
  contentInput.className = 'form-control mb-2';
  contentInput.required = true;

  const submitButton = document.createElement('button');
  submitButton.type= 'submit';
  submitButton.innerHTML = 'Submit';
  submitButton.className = 'btn btn-info btn-sm';

  form.appendChild(nameInput);
  form.appendChild(contentInput);
  form.appendChild(submitButton);

  commentText.appendChild(form);
}
