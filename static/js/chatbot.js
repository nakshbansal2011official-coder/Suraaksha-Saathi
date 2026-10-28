/**
 * Surakshaa Saathi — Cyber Guide AI Assistant
 * Universal Conversational Intelligence + Real-Time Cyber Triage,
 * Voice Recognition (SpeechRecognition), Voice Synthesis (TTS),
 * and Screenshot / Document Inspection.
 */

class CyberGuideChatbot {
  constructor() {
    this.history = [];
    this.isListening = false;
    this.recognition = null;
    this.speechSynthesis = window.speechSynthesis;
    this.currentUtterance = null;
    this.pendingAttachment = null;

    this.initVoiceRecognition();
    this.bindDOM();
  }

  initVoiceRecognition() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
      this.recognition = new SpeechRecognition();
      this.recognition.continuous = false;
      this.recognition.interimResults = false;
      this.recognition.lang = "en-IN"; // Default to Indian English or Hindi

      this.recognition.onstart = () => {
        this.isListening = true;
        this.updateMicUI(true);
      };

      this.recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        const input = document.getElementById("chat-user-input");
        if (input) {
          input.value = transcript;
          input.focus();
        }
      };

      this.recognition.onerror = (e) => {
        console.warn("Speech recognition error:", e.error);
        this.isListening = false;
        this.updateMicUI(false);
      };

      this.recognition.onend = () => {
        this.isListening = false;
        this.updateMicUI(false);
      };
    }
  }

  toggleVoiceInput() {
    if (!this.recognition) {
      alert("Voice input is not supported in this browser. Please use Google Chrome or Microsoft Edge.");
      return;
    }
    if (this.isListening) {
      this.recognition.stop();
    } else {
      // Map current language
      const curLang = window.i18n ? window.i18n.currentLang : "hi";
      const langMap = {
        hi: "hi-IN",
        bn: "bn-IN",
        te: "te-IN",
        mr: "mr-IN",
        ta: "ta-IN",
        ur: "ur-IN",
        gu: "gu-IN",
        kn: "kn-IN",
        ml: "ml-IN",
        pa: "pa-IN"
      };
      this.recognition.lang = langMap[curLang] || "en-IN";
      try {
        this.recognition.start();
      } catch (e) {
        console.error(e);
      }
    }
  }

  updateMicUI(active) {
    const micBtn = document.getElementById("chat-mic-btn");
    if (!micBtn) return;
    if (active) {
      micBtn.classList.add("bg-rose-600", "text-white", "animate-pulse");
      micBtn.classList.remove("text-slate-400");
    } else {
      micBtn.classList.remove("bg-rose-600", "text-white", "animate-pulse");
      micBtn.classList.add("text-slate-400");
    }
  }

  speakText(text) {
    if (!this.speechSynthesis) return;

    if (this.speechSynthesis.speaking) {
      this.speechSynthesis.cancel();
      return;
    }

    // Strip markdown formatting for cleaner speech synthesis
    const cleanText = text.replace(/[*#_`>]/g, "").replace(/\n/g, ". ");
    this.currentUtterance = new SpeechSynthesisUtterance(cleanText);
    this.currentUtterance.rate = 1.0;
    this.currentUtterance.pitch = 1.0;

    this.speechSynthesis.speak(this.currentUtterance);
  }

  stopSpeech() {
    if (this.speechSynthesis && this.speechSynthesis.speaking) {
      this.speechSynthesis.cancel();
    }
  }

  bindDOM() {
    const sendBtn = document.getElementById("chat-send-btn");
    const input = document.getElementById("chat-user-input");
    const micBtn = document.getElementById("chat-mic-btn");
    const fileInput = document.getElementById("chat-file-upload");
    const newChatBtn = document.getElementById("chat-new-btn");

    if (sendBtn) {
      sendBtn.addEventListener("click", () => this.handleSendMessage());
    }

    if (input) {
      input.addEventListener("keydown", (e) => {
        if (e.key === "Enter" && !e.shiftKey) {
          e.preventDefault();
          this.handleSendMessage();
        }
      });
    }

    if (micBtn) {
      micBtn.addEventListener("click", () => this.toggleVoiceInput());
    }

    if (fileInput) {
      fileInput.addEventListener("change", (e) => {
        const file = e.target.files[0];
        if (file) {
          this.pendingAttachment = {
            name: file.name,
            size: file.size,
            type: file.type
          };
          this.showAttachmentPill(file.name);
        }
      });
    }

    if (newChatBtn) {
      newChatBtn.addEventListener("click", () => {
        this.history = [];
        const msgContainer = document.getElementById("chat-messages");
        if (msgContainer) {
          msgContainer.innerHTML = `
            <div class="chat-bubble-assistant flex gap-3 p-4 rounded-2xl bg-white/5 border border-white/10 max-w-2xl text-slate-200">
              <div class="w-8 h-8 rounded-full bg-cyan-500/20 text-cyan-400 flex items-center justify-center shrink-0 font-bold text-sm">
                SS
              </div>
              <div>
                <p class="font-semibold text-cyan-400 text-sm mb-1">Surakshaa Saathi Cyber Guide</p>
                <p class="text-sm leading-relaxed">
                  Namaste! I am your AI Cyber Safety Assistant. I can help you evaluate suspicious payment requests, understand Digital Arrest threats, check unfamiliar links or APKs, and guide you on emergency reporting to Helpline <strong>1930</strong>.
                </p>
              </div>
            </div>
          `;
        }
      });
    }

    // Quick Prompt Buttons
    document.querySelectorAll(".quick-prompt-pill").forEach(pill => {
      pill.addEventListener("click", () => {
        const promptText = pill.getAttribute("data-prompt") || pill.textContent.trim();
        if (input) {
          input.value = promptText;
          this.handleSendMessage();
        }
      });
    });
  }

  showAttachmentPill(name) {
    const previewContainer = document.getElementById("chat-attachment-preview");
    if (!previewContainer) return;
    previewContainer.classList.remove("hidden");
    previewContainer.innerHTML = `
      <div class="inline-flex items-center gap-2 px-3 py-1 bg-cyan-500/20 border border-cyan-500/40 rounded-full text-xs text-cyan-300">
        <span>📎 ${name}</span>
        <button id="remove-attach-btn" class="hover:text-rose-400 font-bold">&times;</button>
      </div>
    `;
    document.getElementById("remove-attach-btn").addEventListener("click", () => {
      this.pendingAttachment = null;
      previewContainer.classList.add("hidden");
      previewContainer.innerHTML = "";
      const fileInput = document.getElementById("chat-file-upload");
      if (fileInput) fileInput.value = "";
    });
  }

  async handleSendMessage() {
    const input = document.getElementById("chat-user-input");
    if (!input) return;

    const message = input.value.trim();
    const attachment = this.pendingAttachment;

    if (!message && !attachment) return;

    // Clear composer
    input.value = "";
    this.pendingAttachment = null;
    const previewContainer = document.getElementById("chat-attachment-preview");
    if (previewContainer) {
      previewContainer.classList.add("hidden");
      previewContainer.innerHTML = "";
    }
    const fileInput = document.getElementById("chat-file-upload");
    if (fileInput) fileInput.value = "";

    // Append user message
    this.appendMessage("user", message, attachment);

    // Show typing state
    this.showTypingIndicator();

    try {
      const resp = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: message,
          history: this.history,
          language: window.i18n ? window.i18n.currentLang : "hi",
          attachment: attachment
        })
      });

      const data = await resp.json();
      this.removeTypingIndicator();

      if (data.response) {
        this.appendMessage("assistant", data.response);
        this.history.push({ role: "user", content: message });
        this.history.push({ role: "assistant", content: data.response });
      } else {
        this.appendMessage("assistant", "⚠️ An error occurred while retrieving assistance. Please call Helpline 1930 for immediate safety support.");
      }
    } catch (e) {
      this.removeTypingIndicator();
      this.appendMessage("assistant", "⚠️ Network connection interrupted. If this is an urgent financial cyber fraud, call Helpline 1930 or your bank immediately.");
    }
  }

  appendMessage(role, text, attachment) {
    const container = document.getElementById("chat-messages");
    if (!container) return;

    const msgDiv = document.createElement("div");
    msgDiv.className = role === "user" ? "flex justify-end" : "flex justify-start";

    let attachHTML = "";
    if (attachment) {
      attachHTML = `
        <div class="mb-2 px-3 py-1.5 bg-black/30 border border-white/10 rounded-lg text-xs text-cyan-300 flex items-center gap-2">
          <span>📄 Attached for Inspection: <strong>${attachment.name}</strong></span>
        </div>
      `;
    }

    if (role === "user") {
      msgDiv.innerHTML = `
        <div class="max-w-xl bg-gradient-to-r from-violet-600 to-indigo-600 text-white p-4 rounded-2xl rounded-tr-sm shadow-md text-sm leading-relaxed">
          ${attachHTML}
          <p class="whitespace-pre-wrap">${this.escapeHTML(text)}</p>
        </div>
      `;
    } else {
      const msgId = "msg-" + Math.random().toString(36).substr(2, 9);
      // Format simple markdown into HTML
      const formatted = this.formatMarkdown(text);
      msgDiv.innerHTML = `
        <div class="flex gap-3 max-w-2xl bg-slate-900/80 border border-slate-700/60 p-4 rounded-2xl rounded-tl-sm text-slate-100 shadow-lg">
          <div class="w-8 h-8 rounded-full bg-gradient-to-br from-cyan-500 to-teal-500 text-slate-950 flex items-center justify-center shrink-0 font-bold text-xs shadow-sm">
            SS
          </div>
          <div class="flex-1 overflow-hidden">
            <div class="flex items-center justify-between mb-2">
              <span class="text-xs font-semibold text-cyan-400">Surakshaa Saathi Cyber Guide</span>
              <div class="flex items-center gap-2">
                <button class="speak-btn text-slate-400 hover:text-cyan-300 text-xs px-2 py-0.5 rounded bg-white/5" title="Read Aloud (Text to Speech)" data-target="${msgId}">
                  🔊 Listen
                </button>
                <button class="copy-btn text-slate-400 hover:text-cyan-300 text-xs px-2 py-0.5 rounded bg-white/5" title="Copy Message" data-target="${msgId}">
                  📋 Copy
                </button>
              </div>
            </div>
            <div id="${msgId}" class="prose prose-invert prose-sm text-slate-200 leading-relaxed space-y-2">
              ${formatted}
            </div>
            <div class="mt-3 pt-2 border-t border-white/5 flex items-center justify-between text-xs text-slate-400">
              <span>National Cyber Helpline: <strong class="text-rose-400">1930</strong></span>
              <a href="https://cybercrime.gov.in" target="_blank" class="text-cyan-400 hover:underline">cybercrime.gov.in ↗</a>
            </div>
          </div>
        </div>
      `;
    }

    container.appendChild(msgDiv);
    container.scrollTop = container.scrollHeight;

    // Attach copy & speak event listeners
    msgDiv.querySelectorAll(".copy-btn").forEach(btn => {
      btn.addEventListener("click", () => {
        const targetId = btn.getAttribute("data-target");
        const contentEl = document.getElementById(targetId);
        if (contentEl) {
          navigator.clipboard.writeText(contentEl.innerText);
          btn.textContent = "✓ Copied";
          setTimeout(() => { btn.textContent = "📋 Copy"; }, 2000);
        }
      });
    });

    msgDiv.querySelectorAll(".speak-btn").forEach(btn => {
      btn.addEventListener("click", () => {
        const targetId = btn.getAttribute("data-target");
        const contentEl = document.getElementById(targetId);
        if (contentEl) {
          this.speakText(contentEl.innerText);
        }
      });
    });
  }

  showTypingIndicator() {
    const container = document.getElementById("chat-messages");
    if (!container) return;

    const ind = document.createElement("div");
    ind.id = "typing-indicator";
    ind.className = "flex gap-2 items-center p-3 text-slate-400 text-xs";
    ind.innerHTML = `
      <div class="w-6 h-6 rounded-full bg-cyan-500/20 text-cyan-400 flex items-center justify-center font-bold text-xs">SS</div>
      <span class="flex gap-1">
        <span class="w-2 h-2 rounded-full bg-cyan-400 animate-bounce"></span>
        <span class="w-2 h-2 rounded-full bg-cyan-400 animate-bounce [animation-delay:0.2s]"></span>
        <span class="w-2 h-2 rounded-full bg-cyan-400 animate-bounce [animation-delay:0.4s]"></span>
      </span>
      <span>Cyber Guide is analyzing...</span>
    `;
    container.appendChild(ind);
    container.scrollTop = container.scrollHeight;
  }

  removeTypingIndicator() {
    const ind = document.getElementById("typing-indicator");
    if (ind) ind.remove();
  }

  escapeHTML(str) {
    return str.replace(/[&<>'"]/g, 
      tag => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;' }[tag] || tag)
    );
  }

  formatMarkdown(text) {
    let html = text
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*(.*?)\*/g, '<em>$1</em>')
      .replace(/`(.*?)`/g, '<code class="px-1.5 py-0.5 bg-black/40 text-cyan-300 rounded font-mono text-xs">$1</code>')
      .replace(/^### (.*$)/gim, '<h3 class="text-base font-bold text-cyan-300 mt-2 mb-1">$1</h3>')
      .replace(/^## (.*$)/gim, '<h2 class="text-lg font-bold text-cyan-300 mt-3 mb-1">$1</h2>')
      .replace(/^# (.*$)/gim, '<h1 class="text-xl font-bold text-cyan-300 mt-3 mb-1">$1</h1>')
      .replace(/^\s*• (.*$)/gim, '<li class="ml-4 list-disc text-slate-200">$1</li>')
      .replace(/^\s*\d+\.\s*(.*$)/gim, '<li class="ml-4 list-decimal text-slate-200">$1</li>');

    return html.split("\n\n").map(p => `<p>${p}</p>`).join("");
  }
}

document.addEventListener("DOMContentLoaded", () => {
  window.cyberGuideChatbot = new CyberGuideChatbot();
});

