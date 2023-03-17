const form = document.querySelector("form");
const chatcontainer = document.querySelector("#chat_container");

let loadInterval;

// load messages. render 3 dots while message loads
function messageLoader(element) {
  // make sure it's empty
  element.textContent = "";

  // every
  loadInterval = setInterval(() => {
    element.textContent += ".";
    // if loading indicator reach 3 dots reset
    if (element.textContent === "....") {
      element.textContent = "";
    }
  }, 300);
}

// generate unique id for each message
function generateMessageId() {
  return "id-" + Date.now().toString(36) + Math.random().toString(36).slice(2);
}

function messageView(isAi, value, uid) {
  return `
        <div class="wrapper" ${isAi && "ai"}">
            <div class="chat">
               
                <div class="message" id=${uid}>
                    ${value}
                </div>
            </div>
        </div>
        `;
}

const handleSubmit = async (e) => {
  // dont reload page
  e.preventDefault();

  const data = new FormData(form);

  // Resize textarea to its original size
  form.querySelector("textarea").style.height = "auto";

  // user
  chatcontainer.innerHTML += messageView(false, data.get("prompt"));

  form.reset();

  // bot
  const uid = generateMessageId();
  chatcontainer.innerHTML += messageView(true, " ", uid);

  chatcontainer.scrollTop = chatcontainer.scrollHeight;

  const messageDiv = document.getElementById(uid);

  messageLoader(messageDiv);
};

// adjust textarea based on content length
function textAreaAdjust(e) {
  e.style.height = "1px";
  e.style.height = 5 + e.scrollHeight + "px";
}

// user press submit button
form.addEventListener("submit", handleSubmit);
// user press 'enter' on the keyboard
form.addEventListener("keyup", (e) => {
  if (e.code === "Enter") {
    handleSubmit(e);
  }
});
