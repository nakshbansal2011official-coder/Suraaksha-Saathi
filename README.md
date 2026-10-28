# 🛡️ Surakshaa Saathi (सुरक्षा साथी)
### *A Premium National-Level Indian Cyber Safety, Awareness & Digital Defense Platform*

> **Official Tagline:** *"Stay Aware. Stay Secure. Stay Ahead."*  
> **Mission:** Empowering 1.4 billion Indian citizens, students, parents, teachers, seniors, and working professionals with deep scam awareness, practical digital defense, daily examinations, verified certificates, and direct access to official cybercrime helplines.

---

## 🌟 Key Highlights & Capabilities

1. **Exact 13 Official Indian Languages Localization:**
   - Full central localization with zero language mixing.
   - Languages: **Hindi (हिन्दी)**, **Bengali (বাংলা)**, **Telugu (తెలుగు)**, **Marathi (मराठी)**, **Tamil (தமிழ்)**, **Urdu (اردو - with Right-to-Left RTL layout)**, **Gujarati (ગુજરાતી)**, **Kannada (ಕನ್ನಡ)**, **Odia (ଓଡ଼ିଆ)**, **Malayalam (മലയാളം)**, **Punjabi (ਪੰਜਾਬੀ)**, **Assamese (অসমীয়া)**, **Sanskrit (संस्कृतम्)**.
   - The brand name *"Surakshaa Saathi"* is preserved across all languages.

2. **Mandatory Participant Registration — No OTP Verification:**
   - Direct, accessible onboarding collecting Full Name, Country (typed text), State/UT (typed text), City (typed text), Phone Number with country code, Email Address, and Preferred Language.
   - No SMS codes, OTPs, or barriers to public education.
   - Instant entry upon valid data submission with returning visitor detection.

3. **280+ Scam Awareness Scenario Library:**
   - Pre-seeded with over 280 distinct, detailed real-world scenarios across 22 critical categories (UPI/Banking fraud, Reverse QR collection, Digital Arrest intimidation, WhatsApp screen-sharing, Fake job tasks, Predatory loan apps, AI voice clones, Senior citizen utility threats, etc.).
   - Defensive breakdowns, psychological manipulation analyses, actionable victim steps, things to avoid, long-term risk reduction, and official reporting procedures.
   - Real-time search, category filtering, risk levels, and target audience facets.

4. **Daily Cyber-Awareness Examination (IST Asia/Kolkata Cycle):**
   - Strictly enforces **1 attempt per participant per day (IST)** on the backend database.
   - Instant educational feedback and defensive explanations post-submission.
   - Prevention of double-submissions or score tampering upon page refresh.

5. **Automatic High-Resolution Certificate Generation:**
   - Clear threshold logic: Total marks $T = 10$, Score $S$:
     - $S = T$: **Certificate of Appreciation**
     - $S = T - 1$: **Certificate of Appreciation**
     - $S = T - 2$: **Certificate of Appreciation**
     - Otherwise: **Certificate of Participation**
   - High-fidelity formal certificate rendering with official gold/teal security seals, national watermark, unique reference ID (`SS-2026-XXXXXXXX`), date, and QR verification.
   - Instant direct download as **Printable PDF** and **High-Resolution PNG**.
   - Transactional email dispatch handler with accurate delivery logging and safe fallback.

6. **Surakshaa Saathi Cyber Guide (AI Assistant):**
   - Universal conversational intelligence + specialized cyber safety triage.
   - Voice Recognition (Microphone input via Web Speech API).
   - Text-to-Speech (Audio read-aloud via Web Speech Synthesis API).
   - Attachment Inspector for screenshots, APKs, and documents.
   - Configurable OpenAI / Responses API integration + resilient built-in Cyber Reasoning Core ensuring 100% immediate availability without external API dependencies.

7. **Host-Controlled Cyber Safety Poster Gallery:**
   - Strictly host-owned: only verified administrators can publish or remove posters.
   - 6 Pre-loaded high-resolution (1200x1600) awareness posters ready for download in clean PNG format.

8. **Five-Star Citizen Review & Feedback Panel:**
   - Free-form typed profession field (teacher, student, doctor, homemaker, farmer, etc.).
   - Interactive 1–5 star rating with client-side validation and automated moderation filters.

9. **Emergency "Golden Hour" 1930 Triage & Official Government Resources:**
   - Prominent directive to contact **Helpline 1930** and freeze transactions within the first 2 hours.
   - Verified links to the National Cyber Crime Reporting Portal (`https://cybercrime.gov.in`), CERT-In, RBI Ombudsman, and Consumer Helpline with safe exit confirmation modals.

10. **Secure Host Administrator Dashboard:**
    - Protected by SHA-256 token authentication (Default credentials: `Surakshaa@2026`).
    - Live monitoring metrics, poster management, scenario publishing, review moderation, and system settings.

11. **Signature 3D Moving Canvas Background:**
    - Custom WebGL/Canvas mathematical animation: flowing multilayered aurora gradients in violet, teal, and emerald, curved 3D energy ribbons, rotating translucent security shield, interactive mouse/touch parallax particles, and reduced-motion accessibility controls.

---

## 🛠️ Architecture & Technical Stack

- **Backend:** Python 3.11 with Flask, SQLite3, and native hashlib/smtplib.
- **Frontend:** Responsive Single-Page Application (HTML5, Tailwind CSS, Lucide icons, jsPDF, Canvas Confetti).
- **Database:** SQLite (`surakshaa_saathi.db`) with tables for participants, quiz attempts, certificates, scam scenarios, posters, reviews, daily tips, and admin configs.
- **Timezone:** Strict India Standard Time (`Asia/Kolkata` - UTC+5:30) for daily quiz resets and certificate issuances.

---

## 🚀 Quick Start & Local Execution

### 1. Prerequisites
Ensure Python 3.10+ is installed on your computer.

### 2. Verify / Install Dependencies
```bash
pip install Flask requests pillow
```

### 3. Initialize & Seed Database
```bash
# Seed 280+ scam scenarios
python build_scenarios.py

# Seed supporting data (quizzes, tips, posters, reviews)
python seed_data.py

# Generate high-resolution posters (1200x1600 PNG)
python generate_posters.py
```

### 4. Start the Application Server
```bash
python server.py
```
Open your browser and navigate to:  
👉 **`http://localhost:5000`**

---

## 🔒 Administrator Access
- Access the Admin Dashboard by clicking the **Admin 🔒** tab in the navigation bar.
- **Default Master Passcode:** `Surakshaa@2026`
- Once logged in, administrators can publish new posters, update scenarios, moderate reviews, and configure OpenAI API keys.

---

## ☁️ Production Deployment

### Option A: Render / Railway / Docker
1. Push the codebase to a GitHub repository.
2. In your cloud provider dashboard (e.g. Render, Railway, or VPS), set the start command:
   ```bash
   python server.py
   ```
3. Set optional environment variables:
   - `PORT`: `5000` or dynamically assigned `$PORT`
   - `OPENAI_API_KEY`: *(Optional)* Your OpenAI API key for advanced GPT-4o-mini reasoning.
   - `SMTP_HOST`, `SMTP_USER`, `SMTP_PASS`: *(Optional)* If sending automated certificate emails.

### Option B: Vercel (WSGI / Serverless)
1. Configure `vercel.json` with `@vercel/python` pointing to `server.py`.
2. Deploy directly via `vercel deploy`.

---

## 📜 Compliance & Disclaimers
- Surakshaa Saathi is an independent, non-commercial public cybersecurity education initiative.
- Official cybercrime complaints must always be filed through the official Government of India portal: **[https://cybercrime.gov.in](https://cybercrime.gov.in)** or by calling **1930**.
- The platform never solicits passwords, PINs, OTPs, or authentication secrets.

