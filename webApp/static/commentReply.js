function setAttrs(element, attrs) {
  for (const attr in attrs) {
    element.setAttribute(attr, attrs[attr]);
  }
}

function getIncrementedComments(commentText) {
  // takes string like "Comments: 15" and returns "Comments: 16" to let caller update
  // element text accordingly
  let newString = "";
  let commentNumString = "";

  for (const char of commentText) {
    if ("0123456789".includes(char)) {
      commentNumString += char;
    } else {
      newString += char;
    }
  }

  const newNum = parseInt(commentNumString, 10) + 1;

  return newString + newNum;
}

async function makeRequest(url, options) {
  const response = await fetch(url, options);
  const responseData = await response.json();
  return responseData;
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

function makeCommentNode(commentObj) {
  const newComment = document.createElement("div");
  const commentTitle = document.createElement("small");
  const replyButton = document.createElement("button");
  const commentContent = document.createElement("p");

  newComment.className = "container mb-2 mt-2";
  newComment.id = commentObj.id;

  commentTitle.className = "m-0 text-muted";
  commentTitle.innerHTML = `${commentObj.author} — ${commentObj.date} | `;

  replyButton.type = "button";
  replyButton.className = "btn btn-link text-decoration-none btn-sm p-0 pb-1";
  replyButton.innerHTML = "Reply";
  replyButton.addEventListener("click", postReply);

  commentContent.className = "m-0";
  commentContent.innerHTML = commentObj.content;

  commentTitle.appendChild(replyButton);

  newComment.appendChild(commentTitle);
  newComment.appendChild(commentContent);

  return newComment;
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
      replyTo: 0,
    }),
  };

  if (contentElem.checkValidity() && nameElem.checkValidity()) {
    event.preventDefault();

    const respComment = await makeRequest(commentEndpoint, fetchOptions);

    const commentNode = makeCommentNode(respComment);

    const articleElem = document.querySelector("article.post-container");
    const commentFormElem = articleElem.querySelector("form");
    const firstCommentElem = commentFormElem.nextElementSibling;

    commentFormElem.reset();

    if (firstCommentElem === null) {
      articleElem.appendChild(commentNode);
    } else {
      articleElem.insertBefore(commentNode, firstCommentElem);
    }

    const commentNum = commentFormElem.previousElementSibling;
    const newNum = getIncrementedComments(commentNum.innerHTML);
    commentNum.innerHTML = newNum;
  }
}
