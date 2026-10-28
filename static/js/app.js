/**
 * Surakshaa Saathi — Main Application Orchestrator & Client Router
 * Onboarding Flow (Language -> Registration -> Direct Entry without OTP),
 * Tab Navigation, Profile Management, Emergency Helplines, and Certificate Modals.
 */

class SurakshaaApp {
  constructor() {
    this.currentUser = null;
    this.currentTab = "home";
    this.init();
  }

  async init() {
    this.loadUserSession();
    this.bindNavigation();
    this.bindLanguageSelector();
    this.bindRegistrationForm();
    this.bindProfile();
    this.loadDailyTip();
    this.loadEmergencyResources();

    // Check Onboarding
    const hasOnboarded = localStorage.getItem("surakshaa_onboarded") === "true";
    if (!hasOnboarded && !this.currentUser) {
      this.openWelcomeModal();
    } else {
      this.updateUserGreeting();
    }
  }

  loadUserSession() {
    const raw = localStorage.getItem("surakshaa_user");
    if (raw) {
      try {
        this.currentUser = JSON.parse(raw);
      } catch (e) {
        this.currentUser = null;
      }
    }
  }

  saveUserSession(user) {
    this.currentUser = user;
    localStorage.setItem("surakshaa_user", JSON.stringify(user));
    localStorage.setItem("surakshaa_uuid", user.uuid);
    localStorage.setItem("surakshaa_onboarded", "true");
    this.updateUserGreeting();
  }

  updateUserGreeting() {
    const badge = document.getElementById("nav-user-badge");
    const nameSpan = document.getElementById("nav-user-name");
    if (!badge || !nameSpan) return;

    if (this.currentUser) {
      badge.classList.remove("hidden");
      nameSpan.textContent = this.currentUser.full_name;
    } else {
      badge.classList.add("hidden");
    }
  }

  switchTab(tabId) {
    this.currentTab = tabId;

    // Hide all sections
    document.querySelectorAll(".page-section").forEach(sec => {
      sec.classList.add("hidden");
    });

    // Show active section
    const activeSec = document.getElementById(`section-${tabId}`);
    if (activeSec) {
      activeSec.classList.remove("hidden");
      window.scrollTo({ top: 0, behavior: "smooth" });
    }

    // Update active nav styling
    document.querySelectorAll(".nav-link-btn").forEach(btn => {
      if (btn.getAttribute("data-tab") === tabId) {
        btn.classList.add("text-cyan-400", "bg-white/5");
        btn.classList.remove("text-slate-300");
      } else {
        btn.classList.remove("text-cyan-400", "bg-white/5");
        btn.classList.add("text-slate-300");
      }
    });

    // Load section-specific data on activation
    if (tabId === "quiz" && window.dailyQuizEngine) {
      window.dailyQuizEngine.loadTodayQuiz();
    } else if (tabId === "scenarios" && window.scenariosLibrary) {
      window.scenariosLibrary.loadScenarios();
    } else if (tabId === "posters" && window.postersGallery) {
      window.postersGallery.loadPosters();
    } else if (tabId === "reviews" && window.reviewsPanel) {
      window.reviewsPanel.loadReviews();
    } else if (tabId === "profile") {
      this.loadProfileView();
    } else if (tabId === "admin" && window.adminDashboard) {
      if (window.adminDashboard.isLoggedIn()) {
        window.adminDashboard.renderAdminView();
      } else {
        window.adminDashboard.renderLoginView();
      }
    }
  }

  bindNavigation() {
    document.querySelectorAll(".nav-link-btn").forEach(btn => {
      btn.addEventListener("click", () => {
        const tab = btn.getAttribute("data-tab");
        if (tab) this.switchTab(tab);

        // Close mobile drawer if open
        const drawer = document.getElementById("mobile-nav-drawer");
        if (drawer) drawer.classList.add("hidden");
      });
    });

    // Mobile Hamburger
    const menuToggle = document.getElementById("mobile-menu-toggle");
    const drawer = document.getElementById("mobile-nav-drawer");
    const closeDrawer = document.getElementById("close-drawer-btn");

    if (menuToggle && drawer) {
      menuToggle.addEventListener("click", () => {
        drawer.classList.toggle("hidden");
      });
    }
    if (closeDrawer && drawer) {
      closeDrawer.addEventListener("click", () => {
        drawer.classList.add("hidden");
      });
    }

    // Hero Action Buttons
    const heroStartBtn = document.getElementById("hero-get-started-btn");
    if (heroStartBtn) {
      heroStartBtn.addEventListener("click", () => {
        if (!this.currentUser) {
          this.openWelcomeModal();
        } else {
          this.switchTab("quiz");
        }
      });
    }

    const heroExploreBtn = document.getElementById("hero-explore-scenarios-btn");
    if (heroExploreBtn) {
      heroExploreBtn.addEventListener("click", () => this.switchTab("scenarios"));
    }

    const heroChatBtn = document.getElementById("hero-chat-guide-btn");
    if (heroChatBtn) {
      heroChatBtn.addEventListener("click", () => this.switchTab("chatbot"));
    }

    // Reduced Motion Toggle Button
    const motionBtn = document.getElementById("toggle-reduced-motion-btn");
    if (motionBtn) {
      motionBtn.addEventListener("click", () => {
        const current = localStorage.getItem("surakshaa_reduced_motion") === "true";
        const next = !current;
        if (window.surakshaa3D) {
          window.surakshaa3D.setReducedMotion(next);
        }
        motionBtn.textContent = next ? "⚡ Motion: Minimal" : "✨ Motion: Active";
      });
    }
  }

  bindLanguageSelector() {
    const selectorDropdown = document.getElementById("lang-select-dropdown");
    if (selectorDropdown) {
      selectorDropdown.value = window.i18n ? window.i18n.currentLang : "hi";
      selectorDropdown.addEventListener("change", (e) => {
        const lang = e.target.value;
        if (window.i18n) window.i18n.setLanguage(lang);
      });
    }

    // Welcome Screen 13 Languages Grid
    document.querySelectorAll(".welcome-lang-choice").forEach(btn => {
      btn.addEventListener("click", () => {
        const lang = btn.getAttribute("data-lang");
        if (window.i18n) window.i18n.setLanguage(lang);
        document.querySelectorAll(".welcome-lang-choice").forEach(b => b.classList.remove("ring-2", "ring-cyan-400", "bg-cyan-500/20"));
        btn.classList.add("ring-2", "ring-cyan-400", "bg-cyan-500/20");

        // Advance to registration step
        document.getElementById("welcome-step-1").classList.add("hidden");
        document.getElementById("welcome-step-2").classList.remove("hidden");
      });
    });
  }

  openWelcomeModal() {
    const modal = document.getElementById("welcome-onboarding-modal");
    if (modal) {
      modal.classList.remove("hidden");
      document.getElementById("welcome-step-1").classList.remove("hidden");
      document.getElementById("welcome-step-2").classList.add("hidden");
    }
  }

  openRegistrationModal() {
    const modal = document.getElementById("welcome-onboarding-modal");
    if (modal) {
      modal.classList.remove("hidden");
      document.getElementById("welcome-step-1").classList.add("hidden");
      document.getElementById("welcome-step-2").classList.remove("hidden");
    }
  }

  bindRegistrationForm() {
    const form = document.getElementById("onboarding-reg-form");
    if (!form) return;

    form.addEventListener("submit", async (e) => {
      e.preventDefault();

      const name = document.getElementById("reg-full-name").value.trim();
      const country = document.getElementById("reg-country").value.trim();
      const state = document.getElementById("reg-state").value.trim();
      const city = document.getElementById("reg-city").value.trim();
      const phone = document.getElementById("reg-phone").value.trim();
      const email = document.getElementById("reg-email").value.trim();
      const lang = window.i18n ? window.i18n.currentLang : "hi";

      if (!name || !country || !state || !city || !phone || !email) {
        alert("Please fill in all required fields.");
        return;
      }

      const submitBtn = document.getElementById("reg-submit-btn");
      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.textContent = "Entering Surakshaa Saathi...";
      }

      try {
        const resp = await fetch("/api/auth/register", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            full_name: name,
            country: country,
            state: state,
            city: city,
            phone: phone,
            email: email,
            preferred_lang: lang
          })
        });

        const data = await resp.json();

        if (resp.ok && data.participant) {
          this.saveUserSession(data.participant);
          const modal = document.getElementById("welcome-onboarding-modal");
          if (modal) modal.classList.add("hidden");
          alert(`Namaste ${data.participant.full_name}! Welcome to Surakshaa Saathi.`);
          this.switchTab("home");
        } else {
          alert(data.error || "Registration could not be completed.");
        }
      } catch (err) {
        alert("Network error during registration.");
      } finally {
        if (submitBtn) {
          submitBtn.disabled = false;
          submitBtn.textContent = "Complete Registration & Enter Platform";
        }
      }
    });

    const closeBtn = document.getElementById("close-onboarding-btn");
    if (closeBtn) {
      closeBtn.addEventListener("click", () => {
        document.getElementById("welcome-onboarding-modal").classList.add("hidden");
      });
    }
  }

  async loadProfileView() {
    if (!this.currentUser) {
      document.getElementById("profile-unauth-view").classList.remove("hidden");
      document.getElementById("profile-auth-view").classList.add("hidden");
      return;
    }

    document.getElementById("profile-unauth-view").classList.add("hidden");
    document.getElementById("profile-auth-view").classList.remove("hidden");

    try {
      const resp = await fetch(`/api/profile?uuid=${encodeURIComponent(this.currentUser.uuid)}`);
      const data = await resp.json();

      if (data.participant) {
        this.saveUserSession(data.participant);
        document.getElementById("prof-name-input").value = data.participant.full_name || "";
        document.getElementById("prof-country-input").value = data.participant.country || "";
        document.getElementById("prof-state-input").value = data.participant.state || "";
        document.getElementById("prof-city-input").value = data.participant.city || "";
        document.getElementById("prof-phone-input").value = data.participant.phone || "";
        document.getElementById("prof-email-input").value = data.participant.email || "";
        document.getElementById("prof-lang-select").value = data.participant.preferred_lang || "hi";
        document.getElementById("prof-reg-date").textContent = data.participant.created_at || "N/A";
      }

      // Quiz History Table
      const historyTable = document.getElementById("profile-quiz-history");
      if (historyTable && data.quiz_history) {
        if (data.quiz_history.length === 0) {
          historyTable.innerHTML = `<tr class="text-slate-400 text-xs"><td colspan="5" class="py-4 text-center">No quiz attempts recorded yet.</td></tr>`;
        } else {
          historyTable.innerHTML = data.quiz_history.map(q => `
            <tr class="border-b border-white/5 text-xs text-slate-300">
              <td class="py-3 px-2 font-mono">${q.quiz_date}</td>
              <td class="py-3 px-2 font-bold text-cyan-400">${q.score} / ${q.total_marks}</td>
              <td class="py-3 px-2 font-mono text-emerald-400">${q.certificate_id || "N/A"}</td>
              <td class="py-3 px-2 text-slate-400">${q.submitted_at ? q.submitted_at.split(" ")[1] : ""}</td>
              <td class="py-3 px-2">
                <button class="view-past-cert-btn text-amber-400 hover:underline" data-cert="${q.certificate_id}" data-score="${q.score}" data-total="${q.total_marks}" data-date="${q.quiz_date}">
                  View Certificate
                </button>
              </td>
            </tr>
          `).join("");

          historyTable.querySelectorAll(".view-past-cert-btn").forEach(btn => {
            btn.addEventListener("click", () => {
              const cNo = btn.getAttribute("data-cert");
              const sc = parseInt(btn.getAttribute("data-score"));
              const tot = parseInt(btn.getAttribute("data-total"));
              const dt = btn.getAttribute("data-date");
              this.openCertificateModal(this.currentUser.full_name, sc, tot, dt, cNo);
            });
          });
        }
      }

    } catch (e) {
      console.error(e);
    }
  }

  bindProfile() {
    const saveBtn = document.getElementById("profile-save-btn");
    if (saveBtn) {
      saveBtn.addEventListener("click", async () => {
        if (!this.currentUser) return;
        const name = document.getElementById("prof-name-input").value.trim();
        const country = document.getElementById("prof-country-input").value.trim();
        const state = document.getElementById("prof-state-input").value.trim();
        const city = document.getElementById("prof-city-input").value.trim();
        const phone = document.getElementById("prof-phone-input").value.trim();
        const email = document.getElementById("prof-email-input").value.trim();
        const lang = document.getElementById("prof-lang-select").value;

        const resp = await fetch("/api/profile?uuid=" + encodeURIComponent(this.currentUser.uuid), {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            full_name: name,
            country: country,
            state: state,
            city: city,
            phone: phone,
            email: email,
            preferred_lang: lang
          })
        });

        if (resp.ok) {
          const data = await resp.json();
          this.saveUserSession(data.participant);
          alert("Profile details updated successfully.");
        }
      });
    }

    const logoutBtn = document.getElementById("profile-logout-btn");
    if (logoutBtn) {
      logoutBtn.addEventListener("click", () => {
        localStorage.removeItem("surakshaa_user");
        localStorage.removeItem("surakshaa_uuid");
        this.currentUser = null;
        this.updateUserGreeting();
        this.switchTab("home");
      });
    }

    const deleteBtn = document.getElementById("profile-delete-btn");
    if (deleteBtn) {
      deleteBtn.addEventListener("click", async () => {
        const confirmDel = confirm("Are you sure you want to request permanent account deletion? This will remove all your quiz and certificate records.");
        if (!confirmDel) return;

        await fetch("/api/profile?uuid=" + encodeURIComponent(this.currentUser.uuid), {
          method: "DELETE"
        });
        localStorage.removeItem("surakshaa_user");
        localStorage.removeItem("surakshaa_uuid");
        localStorage.removeItem("surakshaa_onboarded");
        this.currentUser = null;
        this.updateUserGreeting();
        alert("Your participant account and records have been permanently deleted.");
        this.switchTab("home");
      });
    }
  }

  async loadDailyTip() {
    try {
      const resp = await fetch("/api/daily-tip");
      const data = await resp.json();
      const tip = data.daily_tip;
      if (!tip) return;

      const titleEl = document.getElementById("daily-tip-title");
      const bodyEl = document.getElementById("daily-tip-text");
      const expEl = document.getElementById("daily-tip-explanation");
      const topicEl = document.getElementById("daily-tip-topic");

      if (titleEl) titleEl.textContent = tip.title;
      if (bodyEl) bodyEl.textContent = tip.tip_text;
      if (expEl) expEl.textContent = tip.explanation;
      if (topicEl) topicEl.textContent = tip.related_topic;

      // Share Tip Button
      const shareBtn = document.getElementById("share-daily-tip-btn");
      if (shareBtn) {
        shareBtn.addEventListener("click", () => {
          const text = `Cyber Safety Tip of the Day (${tip.title}): "${tip.tip_text}" - Stay Aware with Surakshaa Saathi!`;
          if (navigator.share) {
            navigator.share({ title: tip.title, text: text });
          } else {
            navigator.clipboard.writeText(text);
            alert("Daily safety tip copied to clipboard!");
          }
        });
      }
    } catch (e) {
      console.error(e);
    }
  }

  async loadEmergencyResources() {
    try {
      const resp = await fetch("/api/resources");
      const data = await resp.json();
      const listContainer = document.getElementById("official-resources-grid");
      if (!listContainer || !data.resources) return;

      listContainer.innerHTML = data.resources.map(r => `
        <div class="p-6 rounded-2xl bg-slate-900/80 border border-slate-700/60 hover:border-cyan-500/50 shadow-md flex flex-col justify-between group">
          <div>
            <div class="flex items-center justify-between gap-2 mb-2">
              <span class="text-xs px-2.5 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-semibold">
                ✓ Verified Authority
              </span>
              <span class="text-[11px] text-slate-500">Checked: ${r.verified_date}</span>
            </div>
            <h4 class="text-base font-bold text-white mb-2 leading-snug group-hover:text-cyan-300">
              ${r.name}
            </h4>
            <p class="text-xs text-slate-300 leading-relaxed mb-3">
              ${r.purpose}
            </p>
            <div class="p-2.5 rounded-xl bg-black/30 border border-white/5 text-xs text-cyan-300 font-medium mb-3">
              📞 ${r.contact}
            </div>
            <p class="text-xs text-slate-400 italic mb-4">
              🛡️ Guidance: ${r.guidance}
            </p>
          </div>
          <button 
            class="open-gov-link-btn w-full py-2.5 rounded-xl bg-cyan-500/10 hover:bg-cyan-500/20 border border-cyan-500/30 text-cyan-300 text-xs font-bold transition-all flex items-center justify-center gap-1.5"
            data-url="${r.website}"
            data-name="${r.name}"
          >
            <span>Open Official Portal</span>
            <span>↗</span>
          </button>
        </div>
      `).join("");

      // Exit Modal handlers
      listContainer.querySelectorAll(".open-gov-link-btn").forEach(btn => {
        btn.addEventListener("click", () => {
          const url = btn.getAttribute("data-url");
          const name = btn.getAttribute("data-name");
          this.openExitModal(url, name);
        });
      });

    } catch (e) {
      console.error(e);
    }
  }

  openExitModal(url, authorityName) {
    const modal = document.getElementById("external-exit-modal");
    const nameEl = document.getElementById("exit-authority-name");
    const urlEl = document.getElementById("exit-target-url");
    const confirmBtn = document.getElementById("confirm-exit-btn");
    const cancelBtn = document.getElementById("cancel-exit-btn");

    if (!modal) return;
    if (nameEl) nameEl.textContent = authorityName;
    if (urlEl) urlEl.textContent = url;

    modal.classList.remove("hidden");

    const proceed = () => {
      window.open(url, "_blank");
      modal.classList.add("hidden");
      confirmBtn.removeEventListener("click", proceed);
    };

    confirmBtn.addEventListener("click", proceed);
    cancelBtn.addEventListener("click", () => {
      modal.classList.add("hidden");
    });
  }

  openCertificateModal(name, score, totalMarks, quizDate, certNumber) {
    const modal = document.getElementById("certificate-view-modal");
    if (!modal) return;

    modal.classList.remove("hidden");

    const certData = window.certificateManager.generateCertificateData(name, score, totalMarks, quizDate, certNumber);
    window.certificateManager.renderToCanvas(certData);

    const pdfBtn = document.getElementById("modal-cert-download-pdf");
    const pngBtn = document.getElementById("modal-cert-download-png");
    const emailBtn = document.getElementById("modal-cert-send-email");
    const closeBtn = document.getElementById("close-cert-modal-btn");

    if (pdfBtn) {
      pdfBtn.onclick = () => window.certificateManager.downloadPDF(certData);
    }
    if (pngBtn) {
      pngBtn.onclick = () => window.certificateManager.downloadPNG(certData);
    }
    if (emailBtn) {
      emailBtn.onclick = async () => {
        emailBtn.textContent = "Checking Email Service...";
        const res = await window.certificateManager.sendEmail(certData.certificateNumber);
        alert(res.message);
        emailBtn.textContent = "✉ Email Status / Retry";
      };
    }
    if (closeBtn) {
      closeBtn.onclick = () => modal.classList.add("hidden");
    }
  }
}

document.addEventListener("DOMContentLoaded", () => {
  window.app = new SurakshaaApp();
});

