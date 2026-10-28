/**
 * Surakshaa Saathi — Host-Controlled Cyber Safety Poster Gallery
 * Strictly host/admin published. Clean high-resolution PNG download support.
 */

class PostersGallery {
  constructor() {
    this.posters = [];
    this.bindDOM();
  }

  async loadPosters() {
    const grid = document.getElementById("posters-grid-container");
    if (!grid) return;

    grid.innerHTML = `
      <div class="col-span-full p-12 text-center text-slate-400">
        <div class="inline-block w-8 h-8 border-4 border-cyan-400 border-t-transparent rounded-full animate-spin mb-3"></div>
        <p>Loading host-published cyber posters...</p>
      </div>
    `;

    try {
      const resp = await fetch("/api/posters");
      const data = await resp.json();
      this.posters = data.posters || [];

      if (this.posters.length === 0) {
        grid.innerHTML = `
          <div class="col-span-full p-12 text-center bg-slate-900/50 rounded-2xl border border-white/5">
            <p class="text-slate-300 font-semibold mb-1">No posters currently published</p>
            <p class="text-xs text-slate-500">Only authorized website administrators can publish public awareness posters.</p>
          </div>
        `;
        return;
      }

      grid.innerHTML = this.posters.map(p => `
        <div class="poster-card bg-slate-900/80 border border-slate-700/60 rounded-2xl overflow-hidden hover:border-cyan-500/50 transition-all duration-300 hover:shadow-xl hover:shadow-cyan-500/10 flex flex-col justify-between group">
          <!-- Poster Preview Image -->
          <div class="relative overflow-hidden bg-slate-950 aspect-[3/4] cursor-pointer view-poster-preview" data-id="${p.id}">
            <img 
              src="${p.image_url}" 
              alt="${p.title}" 
              class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
              loading="lazy"
            />
            <div class="absolute inset-0 bg-gradient-to-t from-slate-950 via-transparent to-transparent opacity-60"></div>
            <span class="absolute top-3 left-3 px-2.5 py-1 rounded-full bg-slate-900/80 backdrop-blur-md text-[11px] font-semibold text-cyan-300 border border-white/10">
              ${p.category}
            </span>
          </div>

          <!-- Poster Meta & Download Button -->
          <div class="p-5 flex-1 flex flex-col justify-between">
            <div>
              <h4 class="text-sm font-bold text-white mb-1.5 leading-snug group-hover:text-cyan-300 transition-colors">
                ${p.title}
              </h4>
              <p class="text-xs text-slate-400 leading-relaxed mb-4 line-clamp-2">
                ${p.description}
              </p>
            </div>

            <div class="pt-3 border-t border-white/5 flex items-center justify-between gap-2">
              <span class="text-[11px] text-slate-500 truncate max-w-[120px]" title="${p.source_refs}">
                ${p.source_refs}
              </span>
              <a 
                href="${p.image_url}" 
                download="${p.title.replace(/[^a-zA-Z0-9]/g, "_")}.png"
                class="px-3 py-1.5 rounded-lg bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold text-xs shadow-md transition-all flex items-center gap-1 shrink-0"
              >
                <span>⬇ Download PNG</span>
              </a>
            </div>
          </div>
        </div>
      `).join("");

      // Attach click to preview
      grid.querySelectorAll(".view-poster-preview").forEach(el => {
        el.addEventListener("click", () => {
          const id = parseInt(el.getAttribute("data-id"));
          const poster = this.posters.find(item => item.id === id);
          if (poster) this.openFullscreenModal(poster);
        });
      });

    } catch (e) {
      console.error(e);
      grid.innerHTML = `
        <div class="col-span-full p-12 text-center text-rose-400 text-xs">
          Failed to load posters. Please retry.
        </div>
      `;
    }
  }

  openFullscreenModal(poster) {
    const modal = document.getElementById("poster-fullscreen-modal");
    const imgEl = document.getElementById("poster-fullscreen-img");
    const titleEl = document.getElementById("poster-fullscreen-title");
    const descEl = document.getElementById("poster-fullscreen-desc");
    const dlBtn = document.getElementById("poster-fullscreen-download-btn");

    if (!modal) return;

    if (imgEl) imgEl.src = poster.image_url;
    if (titleEl) titleEl.textContent = poster.title;
    if (descEl) descEl.textContent = poster.description;
    if (dlBtn) {
      dlBtn.href = poster.image_url;
      dlBtn.download = `${poster.title.replace(/[^a-zA-Z0-9]/g, "_")}.png`;
    }

    modal.classList.remove("hidden");
    document.getElementById("close-poster-modal-btn").addEventListener("click", () => {
      modal.classList.add("hidden");
    });
  }

  bindDOM() {
    // Loaded upon tab navigation
  }
}

document.addEventListener("DOMContentLoaded", () => {
  window.postersGallery = new PostersGallery();
});

