const COMMENT_NUM_TAG = document.querySelector("#comment-num");

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

function incrementCommentTag() {
  COMMENT_NUM_TAG.innerHTML = getIncrementedComments(COMMENT_NUM_TAG.innerHTML);
}

async function makeRequest(url, options) {
  const response = await fetch(url, options);
  const responseData = await response.json();
  return responseData;
}

function createReplyForm() {
  // Event handler for Reply button on all comments on /post/*
  // Creates a form to submit reply
  const commentText = event.target.parentElement.nextElementSibling;

  event.target.disabled = true;

  if (
    commentText.nextElementSibling !== null &&
    commentText.nextElementSibling.tagName === "FORM"
  ) {
    return;
  }

  const fullText = event.target.parentElement.innerHTML;
  const replyTo = fullText.slice(0, fullText.indexOf(" — "));

  const formAttrs = {
    action: "",
    method: "POST",
  };

  const nameAttrs = {
    type: "text",
    name: "name",
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
  nameInput.id = "name";
  nameInput.className = "form-control form-control-sm mb-2";
  nameInput.required = true;

  setAttrs(contentInput, contentAttrs);
  contentInput.id = "content";
  contentInput.className = "form-control form-control-sm mb-2";
  contentInput.required = true;

  submitButton.type = "submit";
  submitButton.innerHTML = "Submit";
  submitButton.className = "btn btn-info btn-sm";
  submitButton.addEventListener("click", postComment);

  form.appendChild(nameInput);
  form.appendChild(contentInput);
  form.appendChild(submitButton);

  const repliesDiv = commentText.nextElementSibling;

  if (repliesDiv === null) {
    commentText.parentElement.appendChild(form);
  } else {
    commentText.parentElement.insertBefore(form, repliesDiv);
  }
}

function makeCommentNode(commentObj, reply = false) {
  const newComment = document.createElement("div");
  const commentTitle = document.createElement("small");
  const replyButton = document.createElement("button");
  const commentContent = document.createElement("p");

  let classString = "container mb-2 mt-2";

  if (reply) {
    classString += " border-left ml-2";
  }

  newComment.className = classString;
  newComment.id = commentObj.id;

  commentTitle.className = "m-0 text-muted";
  commentTitle.innerHTML = `${commentObj.author} — ${commentObj.created} | `;

  replyButton.type = "button";
  replyButton.className = "btn btn-link text-decoration-none btn-sm p-0 pb-1";
  replyButton.innerHTML = "Reply";
  replyButton.addEventListener("click", createReplyForm);

  commentContent.className = "m-0";
  commentContent.innerHTML = commentObj.content;

  commentTitle.appendChild(replyButton);

  newComment.appendChild(commentTitle);
  newComment.appendChild(commentContent);

  return newComment;
}

async function postComment() {
  const commentForm = event.target.parentElement;
  const contentElem = commentForm.elements.content;
  const nameElem = commentForm.elements.name;
  const pathArr = window.location.pathname.split("/");
  const postId = parseInt(pathArr[pathArr.length - 1], 10);
  const commentEndpoint = `${window.location.protocol}//${window.location.host}/api/${postId}/addComment`;

  let repliedTo = 0;

  if (commentForm.parentElement.tagName !== "ARTICLE") {
    repliedTo = parseInt(commentForm.parentElement.id, 10);
  }

  const fetchOptions = {
    method: "POST",
    headers: { "Content-Type": "application/json;charset=utf-8" },
    body: JSON.stringify({
      name: nameElem.value,
      content: contentElem.value,
      replyTo: repliedTo,
      timeFormat: true,
    }),
  };

  if (contentElem.checkValidity() && nameElem.checkValidity()) {
    event.preventDefault();

    const respComment = await makeRequest(commentEndpoint, fetchOptions);

    if (repliedTo === 0) {
      const commentNode = makeCommentNode(respComment);
      const articleElem = document.querySelector("article.post-container");
      const firstCommentElem = commentForm.nextElementSibling;

      if (firstCommentElem === null) {
        articleElem.appendChild(commentNode);
      } else {
        articleElem.insertBefore(commentNode, firstCommentElem);
      }

      commentForm.reset();
    } else {
      const commentNode = makeCommentNode(respComment, true);
      const replyButton = commentForm.parentElement.querySelector(
        "small > button"
      );

      commentForm.parentElement.insertBefore(commentNode, commentForm);
      commentForm.remove();

      replyButton.disabled = false;
    }

    incrementCommentTag();
  }
}
