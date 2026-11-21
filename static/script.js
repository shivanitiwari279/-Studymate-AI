const chat = document.getElementById("chat");
const form = document.getElementById("chatForm");
const input = document.getElementById("messageInput");
const sendBtn = document.getElementById("sendBtn");
const clearBtn = document.getElementById("clearBtn");

function addMessage(text, role, isError = false) {
  const row = document.createElement("div");
  row.className = `message ${role}${isError ? " error" : ""}`;

  const avatar = document.createElement("div");
  avatar.className = "avatar";
  avatar.textContent = role === "user" ? "YOU" : "AI";

  const bubble = document.createElement("div");
  bubble.className = "bubble";
  // textContent prevents model output from being interpreted as HTML.
  bubble.textContent = text;

  row.append(avatar, bubble);
  chat.appendChild(row);
  chat.scrollTop = chat.scrollHeight;
  return row;
}

async function sendMessage(message) {
  const cleanMessage = message.trim();
  if (!cleanMessage) return;

  addMessage(cleanMessage, "user");
  input.value = "";
  input.focus();
  sendBtn.disabled = true;
  sendBtn.textContent = "Thinking...";

  const loadingRow = addMessage("Preparing a response...", "assistant");

  try {
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: cleanMessage })
    });

    const result = await response.json();
    loadingRow.remove();

    if (!response.ok) {
      addMessage(result.error || "Something went wrong.", "assistant", true);
    } else {
      addMessage(result.reply, "assistant");
    }
  } catch (error) {
    loadingRow.remove();
    addMessage("Could not connect to the server. Check that Flask is running.", "assistant", true);
  } finally {
    sendBtn.disabled = false;
    sendBtn.textContent = "Send";
  }
}

form.addEventListener("submit", (event) => {
  event.preventDefault();
  sendMessage(input.value);
});

document.querySelectorAll(".suggestion").forEach((button) => {
  button.addEventListener("click", () => sendMessage(button.textContent));
});

clearBtn.addEventListener("click", () => {
  chat.replaceChildren();
  addMessage("Chat cleared. What would you like to learn?", "assistant");
});
