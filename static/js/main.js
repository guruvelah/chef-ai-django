// ChefAI Django — Main JS (Chat Widget)

// ---- Chat Widget ----
let chatOpen = false;

function toggleChat() {
  chatOpen = !chatOpen;
  const panel = document.getElementById('chatPanel');
  panel.classList.toggle('open', chatOpen);
  if (chatOpen) {
    document.getElementById('chatInput').focus();
    // Hide suggestions after first real message
    if (document.querySelectorAll('.chat-msg').length > 1) {
      const sugg = document.getElementById('chatSuggestions');
      if (sugg) sugg.style.display = 'none';
    }
  }
}

function handleKey(e) {
  if (e.key === 'Enter') sendMessage();
}

function sendQuick(text) {
  document.getElementById('chatInput').value = text;
  sendMessage();
  const sugg = document.getElementById('chatSuggestions');
  if (sugg) sugg.style.display = 'none';
}

async function sendMessage() {
  const input = document.getElementById('chatInput');
  const msg = input.value.trim();
  if (!msg) return;

  const sendBtn = document.getElementById('sendBtn');
  sendBtn.disabled = true;
  input.value = '';

  // Append user message
  appendMessage('user', '🧑', msg);

  // Show typing indicator
  const typingId = appendTyping();

  try {
    const response = await fetch('/api/chat/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCsrfToken(),
      },
      body: JSON.stringify({ message: msg }),
    });

    const data = await response.json();
    removeTyping(typingId);
    appendMessage('ai', '👨‍🍳', data.reply || 'Sorry, I could not process that.');
  } catch (err) {
    removeTyping(typingId);
    appendMessage('ai', '👨‍🍳', 'Connection error. Please try again!');
  }

  sendBtn.disabled = false;
  input.focus();
}

function appendMessage(role, avatar, text) {
  const container = document.getElementById('chatMessages');
  const div = document.createElement('div');
  div.className = `chat-msg ${role}`;
  div.innerHTML = `
    <span class="chat-msg-avatar">${avatar}</span>
    <div class="chat-bubble">${escapeHtml(text)}</div>
  `;
  container.appendChild(div);
  container.scrollTop = container.scrollHeight;
  return div;
}

function appendTyping() {
  const container = document.getElementById('chatMessages');
  const id = 'typing-' + Date.now();
  const div = document.createElement('div');
  div.className = 'chat-msg ai';
  div.id = id;
  div.innerHTML = `
    <span class="chat-msg-avatar">👨‍🍳</span>
    <div class="chat-bubble">
      <div class="typing-dots">
        <span></span><span></span><span></span>
      </div>
    </div>
  `;
  container.appendChild(div);
  container.scrollTop = container.scrollHeight;
  return id;
}

function removeTyping(id) {
  const el = document.getElementById(id);
  if (el) el.remove();
}

function getCsrfToken() {
  const name = 'csrftoken';
  const cookies = document.cookie.split(';');
  for (let c of cookies) {
    const [k, v] = c.trim().split('=');
    if (k === name) return decodeURIComponent(v);
  }
  return '';
}

function escapeHtml(str) {
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

// Close chat on outside click
document.addEventListener('click', function(e) {
  const panel = document.getElementById('chatPanel');
  const fab = document.getElementById('chatFab');
  const btn = document.getElementById('chatToggleBtn');
  if (chatOpen && panel && !panel.contains(e.target) && e.target !== fab && e.target !== btn && !btn?.contains(e.target)) {
    toggleChat();
  }
});
