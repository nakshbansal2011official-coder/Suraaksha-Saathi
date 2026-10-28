/**
 * Surakshaa Saathi — Cyber-Fraud & Scam Scenario Learning Library
 * Comprehensive browsing of 280+ real-world defensive scenarios,
 * instant search, category filtering, risk-level sorting, and detailed view modals.
 */

class ScenariosLibrary {
  constructor() {
    this.currentPage = 1;
    this.limit = 12;
    this.currentCategory = "All";
    this.currentRisk = "All";
    this.currentAudience = "All";
    this.searchQuery = "";
    this.scenariosData = [];

    this.bindDOM();
  }

  async loadScenarios() {
    const listContainer = document.getElementById("scenarios-grid");
    if (!listContainer) return;

    listContainer.innerHTML = `
      <div class="col-span-full p-12 text-center text-slate-400">
        <div class="inline-block w-8 h-8 border-4 border-cyan-400 border-t-transparent rounded-full animate-spin mb-3"></div>
        <p>Loading cyber fraud scenarios...</p>
      </div>
    `;

    try {
      const params = new URLSearchParams({
        page: this.currentPage,
        limit: this.limit,
        category: this.currentCategory,
        risk_level: this.currentRisk,
        audience: this.currentAudience,
        search: this.searchQuery
      });

      const resp = await fetch(`/api/scenarios?${params.toString()}`);
      const data = await resp.json();

      this.scenariosData = data.scenarios || [];
      this.renderScenariosGrid(data);
      this.renderPagination(data);
    } catch (e) {
      console.error(e);
      listContainer.innerHTML = `
        <div class="col-span-full p-12 text-center text-rose-400">
          <p>Failed to load scenarios. Please retry.</p>
        </div>
      `;
    }
  }

  renderScenariosGrid(data) {
    const container = document.getElementById("scenarios-grid");
    if (!container) return;

    if (!data.scenarios || data.scenarios.length === 0) {
      container.innerHTML = `
        <div class="col-span-full p-12 text-center bg-slate-900/50 rounded-2xl border border-white/5">
          <p class="text-slate-300 font-semibold mb-1">No scenarios match your search criteria</p>
          <p class="text-xs text-slate-500 mb-4">Try clearing your filters or searching for terms like 'UPI', 'QR', or 'Arrest'</p>
          <button id="reset-scenarios-filter-btn" class="px-4 py-2 bg-cyan-500/20 hover:bg-cyan-500/30 text-cyan-300 rounded-xl text-xs font-semibold">
            Reset All Filters
          </button>
        </div>
      `;
      const resetBtn = document.getElementById("reset-scenarios-filter-btn");
      if (resetBtn) {
        resetBtn.addEventListener("click", () => this.resetFilters());
      }
      return;
    }

    container.innerHTML = data.scenarios.map(s => {
      const isCritical = s.risk_level === "Critical";
      const riskClass = isCritical 
        ? "bg-rose-500/20 text-rose-400 border-rose-500/30" 
        : "bg-amber-500/20 text-amber-400 border-amber-500/30";

      return `
        <div class="scenario-card flex flex-col justify-between bg-slate-900/80 hover:bg-slate-900 border border-slate-700/60 hover:border-cyan-500/50 p-6 rounded-2xl transition-all duration-300 hover:-translate-y-1 hover:shadow-xl hover:shadow-cyan-500/10 group">
          <div>
            <!-- Top Badges -->
            <div class="flex items-center justify-between gap-2 mb-3">
              <span class="text-xs px-2.5 py-1 rounded-full bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 font-medium truncate max-w-[160px]">
                ${s.category}
              </span>
              <span class="text-xs px-2 py-0.5 rounded border font-semibold ${riskClass}">
                ${s.risk_level}
              </span>
            </div>

            <!-- Title -->
            <h4 class="text-base font-bold text-white group-hover:text-cyan-300 transition-colors mb-2 line-clamp-2">
              ${s.title}
            </h4>

            <!-- Situation Preview -->
            <p class="text-xs text-slate-400 leading-relaxed line-clamp-3 mb-4">
              ${s.situation}
            </p>
          </div>

          <div>
            <div class="pt-3 border-t border-white/5 flex items-center justify-between text-xs text-slate-400">
              <span class="font-mono text-cyan-400/80">${s.scenario_id}</span>
              <button 
                class="view-scenario-btn font-semibold text-cyan-400 hover:text-cyan-300 flex items-center gap-1 group-hover:underline"
                data-id="${s.scenario_id}"
              >
                Learn Defense →
              </button>
            </div>
          </div>
        </div>
      `;
    }).join("");

    // Attach click handlers
    container.querySelectorAll(".view-scenario-btn").forEach(btn => {
      btn.addEventListener("click", () => {
        const scId = btn.getAttribute("data-id");
        this.openScenarioModal(scId);
      });
    });
  }

  renderPagination(data) {
    const pContainer = document.getElementById("scenarios-pagination");
    if (!pContainer) return;

    if (data.total_pages <= 1) {
      pContainer.innerHTML = "";
      return;
    }

    pContainer.innerHTML = `
      <div class="flex items-center justify-center gap-2 mt-8">
        <button 
          id="sc-page-prev" 
          class="px-4 py-2 rounded-xl border border-white/10 text-slate-300 text-xs font-semibold hover:bg-white/5 disabled:opacity-30 disabled:cursor-not-allowed"
          ${data.page <= 1 ? "disabled" : ""}
        >
          ← Prev
        </button>
        <span class="text-xs text-slate-400 px-3">
          Page <strong>${data.page}</strong> of <strong>${data.total_pages}</strong> (${data.total} Scenarios)
        </span>
        <button 
          id="sc-page-next" 
          class="px-4 py-2 rounded-xl border border-white/10 text-slate-300 text-xs font-semibold hover:bg-white/5 disabled:opacity-30 disabled:cursor-not-allowed"
          ${data.page >= data.total_pages ? "disabled" : ""}
        >
          Next →
        </button>
      </div>
    `;

    const prev = document.getElementById("sc-page-prev");
    const next = document.getElementById("sc-page-next");
    if (prev && data.page > 1) {
      prev.addEventListener("click", () => {
        this.currentPage--;
        this.loadScenarios();
      });
    }
    if (next && data.page < data.total_pages) {
      next.addEventListener("click", () => {
        this.currentPage++;
        this.loadScenarios();
      });
    }
  }

  async openScenarioModal(scenarioId) {
    const s = this.scenariosData.find(item => item.scenario_id === scenarioId);
    if (!s) return;

    const modal = document.getElementById("scenario-detail-modal");
    const content = document.getElementById("scenario-detail-content");
    if (!modal || !content) return;

    content.innerHTML = `
      <!-- Header -->
      <div class="flex items-start justify-between gap-4 mb-4 pb-4 border-b border-white/10">
        <div>
          <div class="flex items-center gap-2 mb-2">
            <span class="text-xs px-2.5 py-0.5 rounded-full bg-cyan-500/20 text-cyan-300 border border-cyan-500/30 font-semibold">
              ${s.category}
            </span>
            <span class="text-xs px-2 py-0.5 rounded border font-semibold ${
              s.risk_level === "Critical" ? "bg-rose-500/20 text-rose-400 border-rose-500/30" : "bg-amber-500/20 text-amber-400 border-amber-500/30"
            }">
              Risk: ${s.risk_level}
            </span>
            <span class="text-xs text-slate-400">Target Audience: ${s.target_audience}</span>
          </div>
          <h2 class="text-xl sm:text-2xl font-bold text-white">${s.title}</h2>
          <span class="text-xs font-mono text-cyan-400">ID: ${s.scenario_id} • Reviewed: ${s.last_reviewed}</span>
        </div>
        <button id="close-sc-modal-btn" class="w-8 h-8 rounded-full bg-white/5 hover:bg-white/10 text-slate-300 flex items-center justify-center text-lg">
          &times;
        </button>
      </div>

      <!-- Real-World Situation -->
      <div class="space-y-4 text-sm text-slate-200">
        <div class="p-4 rounded-xl bg-slate-800/80 border border-slate-700">
          <h5 class="text-xs font-bold text-cyan-300 uppercase tracking-wider mb-1">🎭 Real-World Scenario</h5>
          <p class="leading-relaxed">${s.situation}</p>
        </div>

        <!-- How it works defensively -->
        <div class="p-4 rounded-xl bg-slate-800/80 border border-slate-700">
          <h5 class="text-xs font-bold text-violet-300 uppercase tracking-wider mb-1">⚙️ Defensive Breakdown: How The Scam Operates</h5>
          <p class="leading-relaxed">${s.how_works}</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <!-- Warning signs -->
          <div class="p-4 rounded-xl bg-amber-500/10 border border-amber-500/20">
            <h5 class="text-xs font-bold text-amber-400 uppercase tracking-wider mb-2">🚩 Key Warning Signs</h5>
            <p class="text-xs leading-relaxed text-slate-200">${s.warning_signs}</p>
          </div>
          <!-- Psychological manipulation -->
          <div class="p-4 rounded-xl bg-purple-500/10 border border-purple-500/20">
            <h5 class="text-xs font-bold text-purple-400 uppercase tracking-wider mb-2">🧠 Psychological Manipulation</h5>
            <p class="text-xs leading-relaxed text-slate-200">${s.manipulation}</p>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <!-- Victim immediate action -->
          <div class="p-4 rounded-xl bg-emerald-500/10 border border-emerald-500/20">
            <h5 class="text-xs font-bold text-emerald-400 uppercase tracking-wider mb-2">🛡️ What You MUST Do</h5>
            <p class="text-xs leading-relaxed text-slate-200">${s.victim_actions}</p>
          </div>
          <!-- What to avoid -->
          <div class="p-4 rounded-xl bg-rose-500/10 border border-rose-500/20">
            <h5 class="text-xs font-bold text-rose-400 uppercase tracking-wider mb-2">⛔ What You MUST AVOID</h5>
            <p class="text-xs leading-relaxed text-slate-200">${s.avoid_actions}</p>
          </div>
        </div>

        <!-- Long-term risk reduction -->
        <div class="p-4 rounded-xl bg-cyan-500/10 border border-cyan-500/20">
          <h5 class="text-xs font-bold text-cyan-300 uppercase tracking-wider mb-1">🔒 Long-Term Preventive Measures</h5>
          <p class="text-xs leading-relaxed text-slate-200">${s.risk_reduction}</p>
        </div>

        <!-- Official reporting guidance -->
        <div class="p-4 rounded-xl bg-slate-900 border border-cyan-500/30 flex items-center justify-between flex-wrap gap-3">
          <div>
            <h5 class="text-xs font-bold text-white uppercase tracking-wider mb-1">🚨 Official Incident Reporting</h5>
            <p class="text-xs text-slate-300">${s.reporting_guidance}</p>
          </div>
          <a href="https://cybercrime.gov.in" target="_blank" class="px-4 py-2 rounded-xl bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold text-xs shadow-md transition-all">
            Report to Portal ↗
          </a>
        </div>
      </div>
    `;

    modal.classList.remove("hidden");
    document.getElementById("close-sc-modal-btn").addEventListener("click", () => {
      modal.classList.add("hidden");
    });
  }

  resetFilters() {
    this.currentCategory = "All";
    this.currentRisk = "All";
    this.currentAudience = "All";
    this.searchQuery = "";
    this.currentPage = 1;

    const sInput = document.getElementById("scenarios-search-input");
    if (sInput) sInput.value = "";

    const catSelect = document.getElementById("scenarios-category-select");
    if (catSelect) catSelect.value = "All";

    const riskSelect = document.getElementById("scenarios-risk-select");
    if (riskSelect) riskSelect.value = "All";

    this.loadScenarios();
  }

  bindDOM() {
    const searchInput = document.getElementById("scenarios-search-input");
    if (searchInput) {
      let debounceTimer;
      searchInput.addEventListener("input", (e) => {
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(() => {
          this.searchQuery = e.target.value.trim();
          this.currentPage = 1;
          this.loadScenarios();
        }, 350);
      });
    }

    const catSelect = document.getElementById("scenarios-category-select");
    if (catSelect) {
      catSelect.addEventListener("change", (e) => {
        this.currentCategory = e.target.value;
        this.currentPage = 1;
        this.loadScenarios();
      });
    }

    const riskSelect = document.getElementById("scenarios-risk-select");
    if (riskSelect) {
      riskSelect.addEventListener("change", (e) => {
        this.currentRisk = e.target.value;
        this.currentPage = 1;
        this.loadScenarios();
      });
    }
  }
}

document.addEventListener("DOMContentLoaded", () => {
  window.scenariosLibrary = new ScenariosLibrary();
});

