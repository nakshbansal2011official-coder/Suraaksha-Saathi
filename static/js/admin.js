/**
 * Surakshaa Saathi — Secure Host & Administrator Dashboard
 * Real server-side token authentication, stats monitoring,
 * poster publishing/editing, review moderation, scenario updates, and API key management.
 */

class AdminDashboard {
  constructor() {
    this.token = sessionStorage.getItem("surakshaa_admin_token") || "";
    this.bindDOM();
  }

  isLoggedIn() {
    return !!this.token;
  }

  async login(password) {
    try {
      const resp = await fetch("/api/admin/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ password })
      });
      const data = await resp.json();
      if (resp.ok && data.token) {
        this.token = data.token;
        sessionStorage.setItem("surakshaa_admin_token", data.token);
        this.renderAdminView();
        return { success: true };
      } else {
        return { success: false, error: data.error || "Invalid credentials." };
      }
    } catch (e) {
      return { success: false, error: "Network error during authentication." };
    }
  }

  logout() {
    this.token = "";
    sessionStorage.removeItem("surakshaa_admin_token");
    this.renderLoginView();
  }

  async loadStats() {
    if (!this.isLoggedIn()) return;
    try {
      const resp = await fetch("/api/admin/stats", {
        headers: { "Authorization": `Bearer ${this.token}` }
      });
      if (resp.status === 401) {
        this.logout();
        return;
      }
      const data = await resp.json();

      document.getElementById("stat-participants").textContent = data.total_participants || "0";
      document.getElementById("stat-quizzes").textContent = data.total_quizzes || "0";
      document.getElementById("stat-certificates").textContent = data.total_certificates || "0";
      document.getElementById("stat-scenarios").textContent = data.total_scenarios || "0";
      document.getElementById("stat-pending-reviews").textContent = data.pending_reviews || "0";
      document.getElementById("stat-posters").textContent = data.total_posters || "0";
      document.getElementById("stat-ist-clock").textContent = data.ist_time || "";
    } catch (e) {
      console.error(e);
    }
  }

  renderLoginView() {
    const loginSection = document.getElementById("admin-login-view");
    const dashSection = document.getElementById("admin-dashboard-view");
    if (loginSection) loginSection.classList.remove("hidden");
    if (dashSection) dashSection.classList.add("hidden");
  }

  renderAdminView() {
    const loginSection = document.getElementById("admin-login-view");
    const dashSection = document.getElementById("admin-dashboard-view");
    if (loginSection) loginSection.classList.add("hidden");
    if (dashSection) dashSection.classList.remove("hidden");

    this.loadStats();
    this.loadAdminPosters();
    this.loadPendingReviews();
  }

  async loadAdminPosters() {
    const tableBody = document.getElementById("admin-posters-table-body");
    if (!tableBody) return;

    try {
      const resp = await fetch("/api/posters");
      const data = await resp.json();
      const posters = data.posters || [];

      tableBody.innerHTML = posters.map(p => `
        <tr class="border-b border-white/5 text-xs text-slate-300">
          <td class="py-3 px-2 font-mono">${p.id}</td>
          <td class="py-3 px-2 font-semibold text-white">${p.title}</td>
          <td class="py-3 px-2">${p.category}</td>
          <td class="py-3 px-2">
            <span class="px-2 py-0.5 rounded text-[11px] font-bold ${p.published ? "bg-emerald-500/20 text-emerald-400" : "bg-slate-700 text-slate-400"}">
              ${p.published ? "Published" : "Draft"}
            </span>
          </td>
          <td class="py-3 px-2 flex items-center gap-2">
            <button class="toggle-poster-btn text-cyan-400 hover:underline" data-id="${p.id}" data-pub="${p.published}">
              ${p.published ? "Unpublish" : "Publish"}
            </button>
            <button class="delete-poster-btn text-rose-400 hover:underline" data-id="${p.id}">
              Delete
            </button>
          </td>
        </tr>
      `).join("");

      tableBody.querySelectorAll(".toggle-poster-btn").forEach(btn => {
        btn.addEventListener("click", async () => {
          const id = btn.getAttribute("data-id");
          const curPub = btn.getAttribute("data-pub") === "1";
          await fetch(`/api/admin/posters/${id}`, {
            method: "PUT",
            headers: {
              "Content-Type": "application/json",
              "Authorization": `Bearer ${this.token}`
            },
            body: JSON.stringify({ published: !curPub })
          });
          this.loadAdminPosters();
          if (window.postersGallery) window.postersGallery.loadPosters();
        });
      });

      tableBody.querySelectorAll(".delete-poster-btn").forEach(btn => {
        btn.addEventListener("click", async () => {
          if (!confirm("Are you sure you want to delete this poster?")) return;
          const id = btn.getAttribute("data-id");
          await fetch(`/api/admin/posters/${id}`, {
            method: "DELETE",
            headers: { "Authorization": `Bearer ${this.token}` }
          });
          this.loadAdminPosters();
          if (window.postersGallery) window.postersGallery.loadPosters();
        });
      });

    } catch (e) {
      console.error(e);
    }
  }

  async loadPendingReviews() {
    const container = document.getElementById("admin-reviews-list");
    if (!container) return;

    try {
      const resp = await fetch("/api/reviews");
      const data = await resp.json();
      const reviews = data.reviews || [];

      container.innerHTML = reviews.slice(0, 8).map(r => `
        <div class="p-3 rounded-xl bg-slate-800/60 border border-white/5 flex items-start justify-between gap-3 text-xs">
          <div>
            <div class="flex items-center gap-2 mb-1">
              <span class="font-bold text-white">${r.full_name}</span>
              <span class="text-slate-400">(${r.profession})</span>
              <span class="text-amber-400 font-bold">★ ${r.rating}</span>
            </div>
            <p class="text-slate-300 line-clamp-2">"${r.review_text}"</p>
          </div>
          <button class="delete-review-btn text-rose-400 hover:text-rose-300 font-bold shrink-0 p-1" data-id="${r.id}" title="Remove Review">
            ✕
          </button>
        </div>
      `).join("");

      container.querySelectorAll(".delete-review-btn").forEach(btn => {
        btn.addEventListener("click", async () => {
          const id = btn.getAttribute("data-id");
          if (!confirm("Remove this review from public display?")) return;
          await fetch(`/api/admin/reviews/${id}`, {
            method: "DELETE",
            headers: { "Authorization": `Bearer ${this.token}` }
          });
          this.loadPendingReviews();
          if (window.reviewsPanel) window.reviewsPanel.loadReviews();
        });
      });
    } catch (e) {
      console.error(e);
    }
  }

  bindDOM() {
    const loginForm = document.getElementById("admin-login-form");
    if (loginForm) {
      loginForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const pass = document.getElementById("admin-password-input").value;
        const errEl = document.getElementById("admin-login-error");
        const res = await this.login(pass);
        if (!res.success) {
          if (errEl) {
            errEl.textContent = res.error;
            errEl.classList.remove("hidden");
          }
        } else {
          if (errEl) errEl.classList.add("hidden");
        }
      });
    }

    const logoutBtn = document.getElementById("admin-logout-btn");
    if (logoutBtn) {
      logoutBtn.addEventListener("click", () => this.logout());
    }

    const newPosterForm = document.getElementById("admin-new-poster-form");
    if (newPosterForm) {
      newPosterForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const title = document.getElementById("admin-poster-title").value.trim();
        const category = document.getElementById("admin-poster-cat").value.trim();
        const desc = document.getElementById("admin-poster-desc").value.trim();
        const refs = document.getElementById("admin-poster-refs").value.trim();

        const resp = await fetch("/api/admin/posters", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${this.token}`
          },
          body: JSON.stringify({
            title: title,
            category: category,
            description: desc,
            source_refs: refs,
            image_url: "/static/images/poster_1930_helpline.png"
          })
        });

        if (resp.ok) {
          alert("New safety poster published successfully!");
          newPosterForm.reset();
          this.loadAdminPosters();
          if (window.postersGallery) window.postersGallery.loadPosters();
        }
      });
    }

    const settingsForm = document.getElementById("admin-settings-form");
    if (settingsForm) {
      settingsForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const newPass = document.getElementById("admin-new-password").value.trim();
        const apiKey = document.getElementById("admin-openai-key").value.trim();

        const resp = await fetch("/api/admin/settings", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${this.token}`
          },
          body: JSON.stringify({
            new_password: newPass || undefined,
            openai_api_key: apiKey || undefined
          })
        });

        if (resp.ok) {
          alert("Settings saved successfully.");
          settingsForm.reset();
        }
      });
    }
  }
}

document.addEventListener("DOMContentLoaded", () => {
  window.adminDashboard = new AdminDashboard();
});

