const form = document.querySelector("form");
const chatcontainer = document.querySelector("#chat_container");

let loadInterval;

// load messages. render 3 dots while message loads
function messageLoader(element) {
  // make sure it's empty
  element.textContent = "";

  // every 300ms, add a dot to the elements's text content
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
  // if isAi is true, add the "ai" class to the wrapper div
  const wrapperClass = isAi ? "wrapper ai" : "wrapper";

  // if isAi is true, use Temoc.jpg as the profile picture, otherwise use user.png
  const profilePictureSrc = isAi
    ? "static/chatbot/assets/Temoc.jpg"
    : "static/chatbot/assets/user.png";

  return `
        <div class="wrapper ${wrapperClass}">
            <div class="chat">
              <div class="message-container">
               <div class="profile-picture">
                <img 
                  src="${profilePictureSrc}"
                />
                </div>
                <div class="message" id=${uid}>
                    ${value}
                    </div> 
                  </div>  
                </div> 
            </div>  
        </div>  
        `;
}

const handleSubmit = async (e) => {
  // prevent page from reloading
  e.preventDefault();

  const data = new FormData(form);

  // Resize textarea to its original size
  form.querySelector("textarea").style.height = "auto";

  // add user's message to chat container
  const userMessage = data.get("prompt");
  chatcontainer.innerHTML += messageView(false, userMessage);

  form.reset();

  // add blank message to chat container as placeholder for the chatbot's response
  const uid = generateMessageId();
  chatcontainer.innerHTML += messageView(true, " ", uid);

  chatcontainer.scrollTop = chatcontainer.scrollHeight;

  const messageDiv = document.getElementById(uid);

  // loading indicator
  messageLoader(messageDiv);

  // make a POST request to the server w/ user's message as the payload
  const response = await fetch("/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      prompt: data.get("prompt"),
    }),
  });

  // clear message loader interval
  clearInterval(loadInterval);

  // Get the response from the server as JSON
  const responseData = await response.json();

  // Replace the blank message in the chat container with the chatbot's response
  messageDiv.innerHTML = responseData.output;
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
