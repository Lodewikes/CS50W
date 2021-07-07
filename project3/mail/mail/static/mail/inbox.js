document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', () => compose_email());

  // By default, load the inbox
  load_mailbox('inbox');

  // form event listner
  document.querySelector("#compose-form").addEventListener("submit", sendEmail);
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector("#open-email-view").style.display = "none";
  document.querySelector('#compose-view').style.display = 'block';
  document.getElementById("#compose-body").style.whiteSpace = "pre-wrap";

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function sendEmail(event) {
  event.preventDefault();
  // retrieve fields from form
  const recipients = document.querySelector("#compose-recipients").value;
  const subject = document.querySelector("#compose-subject").value;
  const body = document.querySelector("#compose-body").value;

  // POST data
  fetch("/emails", {
    method: "POST",
    body: JSON.stringify({
      recipients: recipients,
      subject: subject,
      body: body
    }),
  })
  .then(response => response.json())
  .then(result => {
    load_mailbox("sent", result);
  })
  .catch(error => console.log(`sendMailError: ${error}`));
}

function load_mailbox(mailbox) {
  // make sure page does not display old views
  document.querySelector("#open-email-view").innerHTML = "";

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // get emails
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    emails.forEach(email => {
      // create a row div for each email
      const row = document.createElement("div");
      // call fuction to populate row with email
      displayEmails(email, row, mailbox);
      // white if read, grey if unread
      if (!email.read && (mailbox === "inbox" || mailbox === "archive")) {
        row.style.backgroundColor = "#d9d9d9";
      } else {
        row.style.backgroundColor = 'white';
      }
      // add div to email-view
      document.querySelector("#emails-view").appendChild(row)
      // call openEmail function when click on row
      row.addEventListener("click", () => openEmail(email, mailbox));
    })
  })
}

function displayEmails(email, row, mailbox) {
  const rowItem = document.createElement("div");
  const date = document.createElement("div");
  const lineBreak = document.createElement("hr");

  // if sent, get recipients
  // if inbox, get sender
  if (mailbox === "sent") {
    const recipients = document.createElement("b");
    recipients.innerHTML = email["recipients"].join(", ") + " ";
    rowItem.appendChild(recipients);
  }
  else if (mailbox === "inbox" || mailbox === "archive") {
    const sender = document.createElement("b");
    sender.innerHTML = email["sender"] + " ";
    rowItem.appendChild(sender);
  }
  
  // Row styling
  rowItem.style.padding = "5px";
  rowItem.innerHTML += email["subject"];

  // Date styling
  date.innerHTML = email["timestamp"];
  date.style.display = "inline-block";
  date.style.float = "right";
  rowItem.appendChild(date)
  // append each row item to the final row div
  row.appendChild(rowItem);   
  // row.style.backgroundColor = "#d9d9d9";
  row.appendChild(lineBreak);
}

function openEmail(email, mailbox) {
  // make sure page does not display old views i.e clear page
  document.querySelector("#open-email-view").innerHTML = "";
  document.querySelector('#emails-view').innerHTML = "";

  // create html elements for email display
  const sender = document.createElement("div");
  const subject = document.createElement("div");
  const body = document.createElement("div");
  const date = document.createElement("div");

  // create html element for a line 
  const lineBreak = document.createElement("hr");

  // create div containig buttons for buttons
  const buttonContainer = document.createElement("div");
  const unreadBtn = document.createElement("button");
  const archiveBtn = document.createElement("button");
	const replyBtn = document.createElement("button");

  // inbox shows a sender and sentbox shows recipients
  if (mailbox === "inbox") {
    sender.innerHTML = "Sender: " + email.sender;
    // opening an email marks it as read
    fetch(`/emails/${email.id}`, {
      method: "PUT",
      body: JSON.stringify({
        read: true,
      })
    });
  } else if (mailbox === "sent") {
    sender.innerHTML = "Recipients: " + email.recipients;
  } else if (mailbox === "archive") {
    sender.innerHTML = "Recipients: " + email.recipients;
    // opening an email marks it as read
    fetch(`/emails/${email.id}`, {
      method: "PUT",
      body: JSON.stringify({
        read: true,
      })
    });
  }

  // set remaining content
  subject.innerHTML = "subject: " + email.subject;
  body.innerHTML = email.body;
  date.innerHTML = email.timestamp;

  // style elements
  date.style.display = "inline-block"
  date.style.float = "right";

  if (email.read) {
    unreadBtn.textContent = "unread";
  } else {
    unreadBtn.textContent = "read";
  }
  unreadBtn.setAttribute("class", "btn btn-dark");
  unreadBtn.setAttribute("id", "unread-btn");
  unreadBtn.style.marginBottom = "5px";
  unreadBtn.style.marginRight = "10px";

  if (email.archived) {
    archiveBtn.textContent = "unarchive";
  } else {
    archiveBtn.textContent = "archive";
  }
  archiveBtn.setAttribute("class", "btn btn-dark");
  archiveBtn.setAttribute("id", "archive-btn");
  archiveBtn.style.marginBottom = "5px";
  archiveBtn.style.marginRight = "10px";

  replyBtn.setAttribute("class", "btn btn-dark");
  replyBtn.textContent = "reply";
  replyBtn.style.marginBottom = "5px";
  replyBtn.style.marginRight = "10px";

  // set onclick listner for buttons
  archiveBtn.addEventListener("click", () => archiveBtnHandler(email, archiveBtn));
  unreadBtn.addEventListener("click", () => readBtnHandler(email, unreadBtn));
  replyBtn.addEventListener("click", () => replyBtnHandler(email));

  // append elements
  sender.appendChild(date);
  if (mailbox !== "sent") {
    buttonContainer.appendChild(unreadBtn);
    buttonContainer.appendChild(archiveBtn);
    buttonContainer.appendChild(replyBtn);
  }

  // append containing div
  document.querySelector("#open-email-view").appendChild(buttonContainer);
  document.querySelector("#open-email-view").appendChild(sender);
  document.querySelector("#open-email-view").appendChild(lineBreak);
  document.querySelector("#open-email-view").appendChild(subject);
  document.querySelector("#open-email-view").appendChild(lineBreak);
  document.querySelector("#open-email-view").appendChild(body);
}

function archiveBtnHandler(email, btn) {
  // FIXME bug fix: only changes once. reload required to redo eventlistner
  btn.textContent = "";
  if(email.archived) {
    fetch(`/emails/${email.id}`, {
      method: "PUT",
      body: JSON.stringify({
        archived: false,
      })
    });
    btn.textContent = "archive";
  } else {
    fetch(`/emails/${email.id}`, {
      method: "PUT",
      body: JSON.stringify({
        archived: true,
      })
    });
    btn.textContent = "unarchive";
  }
}

function readBtnHandler(email, btn) {
  // FIXME bug fix: only changes once. reload required to redo eventlistner
  btn.textContext = "";
  if(email.read) {
    fetch(`/emails/${email.id}`, {
      method: "PUT",
      body: JSON.stringify({
        read: false,
      })
    });
    btn.textContent = "read";
  } else {
    btn.appendChild(document.createTextNode("mark read"));
    fetch(`/emails/${email.id}`, {
      method: "PUT",
      body: JSON.stringify({
        read: true,
      })
    });
    btn.textContent = "unread";
  }
}

// TODO reply
function replyBtnHandler(email) {
  // FIXME after reply opening email shows blank
  // Show compose view and hide other views
  document.querySelector("#emails-view").style.display = "none";
  document.querySelector("#open-email-view").style.display = "none";
  document.querySelector("#compose-view").style.display = "block";

  // Clear out composition fields
  document.querySelector("#compose-recipients").value = email.sender;
  document.querySelector("#compose-subject").value = ((email.subject.match(/^(Re:)\s/)) ? email.subject : "Re: " + email.subject);
  document.querySelector("#compose-body").value = `On ${email.timestamp} ${email.sender} wrote:\n${email.body}\n-------------------------------------\n`;
}
