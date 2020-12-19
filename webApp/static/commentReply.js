function setAttrs(element, attrs) {
  for (const attr in attrs) {
    element.setAttribute(attr, attrs[attr]);
  }
}

async function makeRequest(url, options) {
  const response = await fetch(url, options);
  const responseData = await response.json();
  return responseData;
}

async function postComment() {
  const commentForm = event.target.parentElement.elements;
  const contentElem = commentForm.content;
  const nameElem = commentForm.name;
  const postId = commentForm.postId.value;
  const commentEndpoint = `${window.location.protocol}//${window.location.host}/addComment/${postId}`;

  const fetchOptions = {
    method: "POST",
    headers: { "Content-Type": "application/json;charset=utf-8" },
    body: JSON.stringify({
      name: nameElem.value,
      content: contentElem.value,
    }),
  };

  if (contentElem.checkValidity() && nameElem.checkValidity()) {
    event.preventDefault();

    const resp = await makeRequest(commentEndpoint, fetchOptions);

    if (resp === 13) {
      // SO OBVIOUSLY this doesn't work much and I should probably clone a node somehow
      // to make a new comment and
      const newComment = document.createElement("div");
      newComment.className = "container mb-2 mt-2";
      newComment.innerHTML = `${nameElem.value} wrote ${contentElem.value}`;

      const articleElem = document.querySelector("article.post-container");
      const firstComment = document.querySelector(
        "article > div.container.mb-2.mt-2"
      );
      articleElem.insertBefore(newComment, firstComment);
    }
  }
}

function postReply() {
  // Event handler for Reply button on all comments on /page/*
  // Creates a form to submit reply
  const commentText = event.target.parentElement.nextElementSibling;

  if (commentText.firstElementChild !== null) {
    return;
  }

  event.target.disabled = true;

  const fullText = event.target.parentElement.innerHTML;
  const replyTo = fullText.slice(0, fullText.indexOf(" — "));

  const formAttrs = {
    action: "",
    method: "POST",
  };

  const nameAttrs = {
    type: "text",
    name: "username",
    placeholder: "username",
  };

  const contentAttrs = {
    name: "content",
    placeholder: `Reply to ${replyTo}...`,
  };

  const form = document.createElement("form");
  const nameInput = document.createElement("input");
  const contentInput = document.createElement("textarea");
  const submitButton = document.createElement("button");

  setAttrs(form, formAttrs);
  form.className = "border rounded mt-2 p-2";

  setAttrs(nameInput, nameAttrs);
  nameInput.id = "username";
  nameInput.className = "form-control form-control-sm mb-2";
  nameInput.required = true;

  setAttrs(contentInput, contentAttrs);
  contentInput.id = "content";
  contentInput.className = "form-control form-control-sm mb-2";
  contentInput.required = true;

  submitButton.type = "submit";
  submitButton.innerHTML = "Submit";
  submitButton.className = "btn btn-info btn-sm";

  form.appendChild(nameInput);
  form.appendChild(contentInput);
  form.appendChild(submitButton);

  commentText.appendChild(form);
}
