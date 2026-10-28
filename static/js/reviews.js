/**
 * Surakshaa Saathi — Five-Star Review & Feedback Panel ("Share Your Experience")
 * Free-form typed profession input, interactive 5-star rating,
 * client validation, moderation status handling, and public reviews display.
 */

class ReviewsPanel {
  constructor() {
    this.selectedRating = 5;
    this.bindDOM();
  }

  async loadReviews() {
    const listContainer = document.getElementById("reviews-list-container");
    const avgScoreEl = document.getElementById("reviews-avg-score");
    const totalCountEl = document.getElementById("reviews-total-count");

    if (!listContainer) return;

    listContainer.innerHTML = `
      <div class="p-8 text-center text-slate-400">
        <div class="inline-block w-6 h-6 border-2 border-cyan-400 border-t-transparent rounded-full animate-spin mb-2"></div>
        <p class="text-xs">Loading citizen reviews...</p>
      </div>
    `;

    try {
      const resp = await fetch("/api/reviews");
      const data = await resp.json();

      if (avgScoreEl) avgScoreEl.textContent = data.average_rating ? data.average_rating.toFixed(1) : "5.0";
      if (totalCountEl) totalCountEl.textContent = `Based on ${data.total_reviews} verified citizen experiences`;

      if (!data.reviews || data.reviews.length === 0) {
        listContainer.innerHTML = `
          <div class="p-8 text-center text-slate-400 text-sm">
            No reviews published yet. Be the first to share your experience!
          </div>
        `;
        return;
      }

      listContainer.innerHTML = data.reviews.map(r => {
        let starsHTML = "";
        for (let i = 1; i <= 5; i++) {
          starsHTML += `<span class="${i <= r.rating ? "text-amber-400" : "text-slate-600"} text-sm">★</span>`;
        }

        return `
          <div class="p-5 rounded-2xl bg-slate-900/80 border border-slate-700/60 shadow-md flex flex-col justify-between">
            <div>
              <div class="flex items-center justify-between mb-2">
                <div class="flex items-center gap-2">
                  <div class="w-8 h-8 rounded-full bg-cyan-500/20 text-cyan-300 font-bold text-xs flex items-center justify-center">
                    ${r.full_name.charAt(0).toUpperCase()}
                  </div>
                  <div>
                    <h5 class="text-sm font-bold text-white leading-tight">${r.full_name}</h5>
                    <span class="text-xs text-slate-400">${r.profession}</span>
                  </div>
                </div>
                <div class="flex gap-0.5">
                  ${starsHTML}
                </div>
              </div>
              <p class="text-xs text-slate-300 leading-relaxed mt-2 whitespace-pre-wrap">
                "${r.review_text}"
              </p>
            </div>
            <div class="mt-3 pt-2 border-t border-white/5 flex items-center justify-between text-[11px] text-slate-500">
              <span>Verified Participant</span>
              <span>${r.created_at ? r.created_at.split(" ")[0] : ""}</span>
            </div>
          </div>
        `;
      }).join("");

    } catch (e) {
      console.error(e);
      listContainer.innerHTML = `
        <div class="p-8 text-center text-rose-400 text-xs">
          Unable to load reviews. Please retry.
        </div>
      `;
    }
  }

  bindDOM() {
    // Star Rating Click handlers
    const stars = document.querySelectorAll(".star-select-btn");
    stars.forEach(btn => {
      btn.addEventListener("click", () => {
        const rating = parseInt(btn.getAttribute("data-rating"));
        this.setRating(rating);
      });
    });

    // Form submit
    const form = document.getElementById("review-submit-form");
    if (form) {
      form.addEventListener("submit", (e) => {
        e.preventDefault();
        this.submitReview();
      });
    }
  }

  setRating(rating) {
    this.selectedRating = rating;
    const stars = document.querySelectorAll(".star-select-btn");
    stars.forEach(btn => {
      const r = parseInt(btn.getAttribute("data-rating"));
      if (r <= rating) {
        btn.classList.add("text-amber-400");
        btn.classList.remove("text-slate-600");
      } else {
        btn.classList.remove("text-amber-400");
        btn.classList.add("text-slate-600");
      }
    });
  }

  async submitReview() {
    const nameInput = document.getElementById("review-author-name");
    const profInput = document.getElementById("review-author-profession");
    const textInput = document.getElementById("review-body-text");
    const feedbackMsg = document.getElementById("review-form-feedback");

    const fullName = nameInput ? nameInput.value.trim() : "";
    const profession = profInput ? profInput.value.trim() : "";
    const text = textInput ? textInput.value.trim() : "";

    if (!fullName) {
      alert("Please enter your full name.");
      return;
    }
    if (!profession) {
      alert("Please enter your profession or occupation (e.g. Student, Teacher, Engineer).");
      return;
    }
    if (!text || text.length < 10) {
      alert("Please enter a meaningful review description (at least 10 characters).");
      return;
    }

    if (feedbackMsg) {
      feedbackMsg.classList.remove("hidden", "text-rose-400", "text-emerald-400");
      feedbackMsg.textContent = "Submitting review...";
    }

    try {
      const resp = await fetch("/api/reviews", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          full_name: fullName,
          profession: profession,
          rating: this.selectedRating,
          review_text: text
        })
      });

      const data = await resp.json();

      if (resp.ok) {
        if (feedbackMsg) {
          feedbackMsg.classList.add("text-emerald-400");
          feedbackMsg.textContent = "✓ Review submitted successfully! Thank you for supporting national cyber safety.";
        }
        if (nameInput) nameInput.value = "";
        if (profInput) profInput.value = "";
        if (textInput) textInput.value = "";
        this.setRating(5);
        this.loadReviews();
      } else {
        if (feedbackMsg) {
          feedbackMsg.classList.add("text-rose-400");
          feedbackMsg.textContent = data.error || "Submission failed.";
        }
      }
    } catch (e) {
      if (feedbackMsg) {
        feedbackMsg.classList.add("text-rose-400");
        feedbackMsg.textContent = "Network error. Please try again.";
      }
    }
  }
}

document.addEventListener("DOMContentLoaded", () => {
  window.reviewsPanel = new ReviewsPanel();
});

