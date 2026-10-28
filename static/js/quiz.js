/**
 * Surakshaa Saathi — Daily Cyber-Awareness Quiz Engine
 * Strictly enforces 1 attempt per participant per day (IST).
 * Randomized questions & options, instant educational feedback,
 * and Certificate qualification.
 */

class DailyQuizEngine {
  constructor() {
    this.quizDate = "";
    this.questions = [];
    this.currentQuestionIdx = 0;
    this.userAnswers = {}; // { questionId: selectedIndex }
    this.completed = false;
    this.existingAttempt = null;

    this.bindDOM();
  }

  async loadTodayQuiz() {
    const user = window.app ? window.app.currentUser : null;
    const uuid = user ? user.uuid : (localStorage.getItem("surakshaa_uuid") || "");

    const quizContainer = document.getElementById("quiz-card-container");
    const statusContainer = document.getElementById("quiz-status-notice");
    if (!quizContainer) return;

    quizContainer.innerHTML = `
      <div class="p-8 text-center text-slate-400">
        <div class="inline-block w-8 h-8 border-4 border-cyan-400 border-t-transparent rounded-full animate-spin mb-3"></div>
        <p>Loading today's national cyber quiz (IST)...</p>
      </div>
    `;

    try {
      const url = uuid ? `/api/quiz/today?uuid=${encodeURIComponent(uuid)}` : "/api/quiz/today";
      const resp = await fetch(url);
      const data = await resp.json();

      this.quizDate = data.quiz_date;
      this.completed = data.completed;
      this.existingAttempt = data.existing_attempt;
      this.questions = data.questions || [];

      // Update Date Indicator
      const dateBadge = document.getElementById("quiz-ist-date-badge");
      if (dateBadge) {
        dateBadge.textContent = `Today: ${this.quizDate} (IST Cycle)`;
      }

      if (this.completed && this.existingAttempt) {
        this.renderCompletedState();
      } else {
        this.renderQuestionView();
      }
    } catch (e) {
      console.error(e);
      quizContainer.innerHTML = `
        <div class="p-8 text-center text-rose-400">
          <p>Unable to load the daily quiz. Please check connection and retry.</p>
        </div>
      `;
    }
  }

  renderQuestionView() {
    const container = document.getElementById("quiz-card-container");
    if (!container || this.questions.length === 0) return;

    const q = this.questions[this.currentQuestionIdx];
    const total = this.questions.length;
    const progressPercent = Math.round(((this.currentQuestionIdx) / total) * 100);

    const selectedOption = this.userAnswers[q.id];

    let optionsHTML = "";
    q.options.forEach((opt, idx) => {
      const isSelected = selectedOption === idx;
      optionsHTML += `
        <button 
          class="quiz-option-btn w-full text-left p-4 rounded-xl border transition-all flex items-start gap-3 ${
            isSelected 
              ? "bg-cyan-500/20 border-cyan-400 text-cyan-200 ring-2 ring-cyan-500/30" 
              : "bg-white/5 border-white/10 text-slate-200 hover:bg-white/10 hover:border-slate-500"
          }"
          data-opt-idx="${idx}"
        >
          <span class="w-6 h-6 rounded-full border flex items-center justify-center shrink-0 text-xs font-bold ${
            isSelected ? "border-cyan-400 bg-cyan-400 text-slate-950" : "border-slate-500 text-slate-400"
          }">
            ${String.fromCharCode(65 + idx)}
          </span>
          <span class="text-sm sm:text-base leading-snug">${opt}</span>
        </button>
      `;
    });

    const isLast = (this.currentQuestionIdx === total - 1);
    const hasAnsweredCurrent = selectedOption !== undefined;

    container.innerHTML = `
      <div class="bg-slate-900/80 border border-slate-700/60 rounded-3xl p-6 sm:p-8 backdrop-blur-xl shadow-2xl">
        <!-- Progress Header -->
        <div class="flex items-center justify-between mb-4 text-xs font-semibold uppercase tracking-wider text-slate-400">
          <span>Question ${this.currentQuestionIdx + 1} of ${total}</span>
          <span class="text-cyan-400">${progressPercent}% Completed</span>
        </div>
        <div class="w-full bg-slate-800 h-2 rounded-full overflow-hidden mb-6">
          <div class="bg-gradient-to-r from-cyan-500 to-violet-500 h-full transition-all duration-300" style="width: ${progressPercent}%;"></div>
        </div>

        <!-- Question Prompt -->
        <h3 class="text-lg sm:text-xl font-bold text-white mb-6 leading-relaxed">
          ${q.question}
        </h3>

        <!-- Options List -->
        <div class="space-y-3 mb-8">
          ${optionsHTML}
        </div>

        <!-- Navigation Buttons -->
        <div class="flex items-center justify-between pt-4 border-t border-white/10">
          <button 
            id="quiz-prev-btn" 
            class="px-5 py-2.5 rounded-xl border border-white/10 text-slate-300 hover:bg-white/5 text-sm font-medium transition-all ${
              this.currentQuestionIdx === 0 ? "opacity-30 cursor-not-allowed" : ""
            }"
            ${this.currentQuestionIdx === 0 ? "disabled" : ""}
          >
            ← Previous
          </button>

          ${
            isLast 
              ? `<button 
                  id="quiz-submit-btn" 
                  class="px-6 py-2.5 rounded-xl bg-gradient-to-r from-emerald-500 to-teal-500 hover:from-emerald-400 hover:to-teal-400 text-slate-950 font-bold text-sm shadow-lg shadow-emerald-500/25 transition-all flex items-center gap-2"
                >
                  Submit Final Quiz & Claim Certificate 🎓
                </button>`
              : `<button 
                  id="quiz-next-btn" 
                  class="px-6 py-2.5 rounded-xl bg-gradient-to-r from-cyan-500 to-violet-600 hover:from-cyan-400 hover:to-violet-500 text-white font-semibold text-sm shadow-lg shadow-cyan-500/20 transition-all flex items-center gap-2"
                >
                  Next Question →
                </button>`
          }
        </div>
      </div>
    `;

    // Event listeners for options
    container.querySelectorAll(".quiz-option-btn").forEach(btn => {
      btn.addEventListener("click", () => {
        const optIdx = parseInt(btn.getAttribute("data-opt-idx"));
        this.userAnswers[q.id] = optIdx;
        this.renderQuestionView();
      });
    });

    const prevBtn = document.getElementById("quiz-prev-btn");
    const nextBtn = document.getElementById("quiz-next-btn");
    const submitBtn = document.getElementById("quiz-submit-btn");

    if (prevBtn && this.currentQuestionIdx > 0) {
      prevBtn.addEventListener("click", () => {
        this.currentQuestionIdx--;
        this.renderQuestionView();
      });
    }

    if (nextBtn) {
      nextBtn.addEventListener("click", () => {
        if (this.userAnswers[q.id] === undefined) {
          alert("Please select an answer option before moving to the next question.");
          return;
        }
        this.currentQuestionIdx++;
        this.renderQuestionView();
      });
    }

    if (submitBtn) {
      submitBtn.addEventListener("click", () => this.submitQuizAttempt());
    }
  }

  async submitQuizAttempt() {
    const user = window.app ? window.app.currentUser : null;
    const uuid = user ? user.uuid : (localStorage.getItem("surakshaa_uuid") || "");

    if (!uuid) {
      alert("Please complete participant registration before submitting the daily quiz.");
      if (window.app) window.app.openRegistrationModal();
      return;
    }

    // Check if all answered
    const unanswered = this.questions.filter(q => this.userAnswers[q.id] === undefined);
    if (unanswered.length > 0) {
      const confirmSubmit = confirm(`You have ${unanswered.length} unanswered questions. Submit anyway?`);
      if (!confirmSubmit) return;
    }

    const container = document.getElementById("quiz-card-container");
    container.innerHTML = `
      <div class="p-12 text-center text-slate-300">
        <div class="inline-block w-10 h-10 border-4 border-emerald-400 border-t-transparent rounded-full animate-spin mb-4"></div>
        <h4 class="text-lg font-bold text-white mb-1">Evaluating Your National Cyber Awareness Score...</h4>
        <p class="text-sm text-slate-400">Verifying answers & generating official certificate.</p>
      </div>
    `;

    try {
      const resp = await fetch("/api/quiz/submit", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          uuid: uuid,
          answers: this.userAnswers
        })
      });

      const data = await resp.json();

      if (!resp.ok) {
        if (data.completed) {
          this.completed = true;
          this.existingAttempt = data.attempt;
          this.renderCompletedState();
        } else {
          alert(data.error || "Submission failed.");
          this.loadTodayQuiz();
        }
        return;
      }

      // Trigger Confetti
      if (window.confetti) {
        window.confetti({
          particleCount: 120,
          spread: 70,
          origin: { y: 0.6 }
        });
      }

      this.completed = true;
      this.existingAttempt = {
        score: data.score,
        total_marks: data.total_marks,
        certificate_id: data.certificate.certificate_number,
        answers: data.answers_review
      };

      this.renderCompletedState(data.certificate, data.answers_review);

    } catch (e) {
      console.error(e);
      alert("Network error while submitting quiz. Please check connection.");
      this.loadTodayQuiz();
    }
  }

  renderCompletedState(newCert, answersReview) {
    const container = document.getElementById("quiz-card-container");
    if (!container) return;

    const attempt = this.existingAttempt || {};
    const score = attempt.score !== undefined ? attempt.score : 0;
    const total = attempt.total_marks || 10;
    const certNumber = attempt.certificate_id || (newCert ? newCert.certificate_number : "");
    const isAppreciation = score >= (total - 2);
    const certTitle = isAppreciation ? "Certificate of Appreciation" : "Certificate of Participation";

    const user = window.app ? window.app.currentUser : null;
    const userName = user ? user.full_name : "Participant";

    // Build educational answers review list
    let reviewHTML = "";
    const answersList = answersReview || attempt.answers || [];
    if (answersList.length > 0) {
      reviewHTML = `
        <div class="mt-8 pt-6 border-t border-white/10">
          <h4 class="text-base font-bold text-white mb-4 flex items-center gap-2">
            <span>📚 Educational Explanations & Answer Review</span>
          </h4>
          <div class="space-y-4 max-h-96 overflow-y-auto pr-2">
            ${answersList.map((a, idx) => `
              <div class="p-4 rounded-xl border ${a.is_correct ? "bg-emerald-500/10 border-emerald-500/30" : "bg-rose-500/10 border-rose-500/30"}">
                <div class="flex items-start justify-between gap-3 mb-2">
                  <p class="text-sm font-semibold text-white">${idx + 1}. ${a.question}</p>
                  <span class="text-xs px-2 py-0.5 rounded font-bold shrink-0 ${a.is_correct ? "bg-emerald-500/20 text-emerald-400" : "bg-rose-500/20 text-rose-400"}">
                    ${a.is_correct ? "✓ Correct (+1)" : "✗ Incorrect (0)"}
                  </span>
                </div>
                <div class="text-xs space-y-1 mb-2">
                  <p class="text-slate-300">Your Answer: <span class="${a.is_correct ? "text-emerald-300 font-semibold" : "text-rose-300 font-semibold"}">${a.options[a.selected_index] || "Unanswered"}</span></p>
                  ${!a.is_correct ? `<p class="text-emerald-300">Correct Answer: <strong>${a.options[a.correct_index]}</strong></p>` : ""}
                </div>
                <div class="p-2.5 rounded bg-black/30 border border-white/5 text-xs text-slate-300 leading-relaxed">
                  <strong class="text-cyan-400">Defensive Insight:</strong> ${a.explanation}
                </div>
              </div>
            `).join("")}
          </div>
        </div>
      `;
    }

    container.innerHTML = `
      <div class="bg-slate-900/90 border border-slate-700/60 rounded-3xl p-6 sm:p-8 backdrop-blur-xl shadow-2xl">
        <div class="text-center mb-6">
          <div class="w-16 h-16 rounded-2xl mx-auto flex items-center justify-center text-3xl mb-4 ${
            isAppreciation 
              ? "bg-amber-500/20 border border-amber-500/40 text-amber-400 shadow-lg shadow-amber-500/20" 
              : "bg-cyan-500/20 border border-cyan-500/40 text-cyan-400"
          }">
            ${isAppreciation ? "🏆" : "🎖️"}
          </div>
          <span class="inline-block px-3 py-1 rounded-full text-xs font-semibold uppercase tracking-wider bg-white/10 text-slate-300 mb-2">
            IST Daily Examination Record
          </span>
          <h3 class="text-2xl font-bold text-white mb-1">
            ${isAppreciation ? "Outstanding Achievement!" : "Commendable Cyber Participation!"}
          </h3>
          <p class="text-sm text-slate-400">
            You have successfully completed today's quiz. (1 attempt per daily cycle rule enforced).
          </p>
        </div>

        <!-- Score Dashboard Box -->
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-6">
          <div class="p-4 rounded-2xl bg-white/5 border border-white/10 text-center">
            <span class="text-xs text-slate-400 block mb-1">Final Score</span>
            <span class="text-2xl font-black text-cyan-400">${score} / ${total}</span>
          </div>
          <div class="p-4 rounded-2xl bg-white/5 border border-white/10 text-center">
            <span class="text-xs text-slate-400 block mb-1">Qualification</span>
            <span class="text-sm font-bold ${isAppreciation ? "text-amber-400" : "text-cyan-300"}">${certTitle}</span>
          </div>
          <div class="p-4 rounded-2xl bg-white/5 border border-white/10 text-center">
            <span class="text-xs text-slate-400 block mb-1">Certificate Ref</span>
            <span class="text-xs font-mono font-bold text-emerald-400">${certNumber || "Generated"}</span>
          </div>
        </div>

        <!-- Action Buttons -->
        <div class="flex flex-wrap items-center justify-center gap-3">
          <button 
            id="view-cert-modal-btn" 
            class="px-6 py-3 rounded-xl bg-gradient-to-r from-amber-500 to-amber-600 hover:from-amber-400 hover:to-amber-500 text-slate-950 font-bold text-sm shadow-lg shadow-amber-500/25 transition-all flex items-center gap-2"
          >
            <span>📜 View & Download Certificate</span>
          </button>
          <button 
            id="share-quiz-btn" 
            class="px-5 py-3 rounded-xl border border-white/10 hover:bg-white/5 text-slate-200 text-sm font-medium transition-all flex items-center gap-2"
          >
            <span>🔗 Share Score</span>
          </button>
        </div>

        ${reviewHTML}
      </div>
    `;

    const viewCertBtn = document.getElementById("view-cert-modal-btn");
    if (viewCertBtn) {
      viewCertBtn.addEventListener("click", () => {
        if (window.app) {
          window.app.openCertificateModal(userName, score, total, this.quizDate, certNumber);
        }
      });
    }

    const shareBtn = document.getElementById("share-quiz-btn");
    if (shareBtn) {
      shareBtn.addEventListener("click", () => {
        const text = `I scored ${score}/${total} in the National Cyber Awareness Examination on Surakshaa Saathi! Test your fraud prevention knowledge at https://cybercrime.gov.in`;
        if (navigator.share) {
          navigator.share({ title: "Surakshaa Saathi Quiz", text: text });
        } else {
          navigator.clipboard.writeText(text);
          alert("Score summary copied to clipboard! Share with family and friends.");
        }
      });
    }
  }

  bindDOM() {
    // Loaded upon tab navigation
  }
}

document.addEventListener("DOMContentLoaded", () => {
  window.dailyQuizEngine = new DailyQuizEngine();
});

