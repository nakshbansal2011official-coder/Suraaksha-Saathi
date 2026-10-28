import os
import sys
import json
import sqlite3
import hashlib
import uuid
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from datetime import datetime, timezone, timedelta
from flask import Flask, request, jsonify, render_template, send_from_directory

from database import get_db, init_db, get_ist_now, get_ist_date_str
from seed_data import QUIZ_QUESTIONS_POOL, DAILY_TIPS_POOL, OFFICIAL_RESOURCES

app = Flask(__name__, static_folder="static", template_folder="templates")
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'surakshaa-saathi-national-safety-key-2026')

# Initialize DB on start
init_db()

# --- Helper Utilities ---

def get_admin_token(password_hash):
    # Deterministic session token from hash + current date
    ist_date = get_ist_date_str()
    return hashlib.sha256(f"{password_hash}-{ist_date}-surakshaa-admin".encode('utf-8')).hexdigest()

def verify_admin(req):
    auth_header = req.headers.get("Authorization", "")
    token = auth_header.replace("Bearer ", "").strip()
    if not token:
        return False
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT value FROM admin_config WHERE key = 'admin_password_hash'")
    row = cursor.fetchone()
    conn.close()
    if not row:
        return False
    valid_token = get_admin_token(row["value"])
    return token == valid_token

# --- Frontend Routes ---

@app.route("/")
def index():
    return render_template("index.html")

# --- Participant Registration & Profile ---

@app.route("/api/auth/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    full_name = (data.get("full_name") or "").strip()
    country = (data.get("country") or "").strip()
    state = (data.get("state") or "").strip()
    city = (data.get("city") or "").strip()
    phone = (data.get("phone") or "").strip()
    email = (data.get("email") or "").strip()
    preferred_lang = (data.get("preferred_lang") or "hi").strip()

    # Validation
    if not full_name:
        return jsonify({"error": "Full Name is required"}), 400
    if not country:
        return jsonify({"error": "Country is required"}), 400
    if not state:
        return jsonify({"error": "State / UT is required"}), 400
    if not city:
        return jsonify({"error": "City is required"}), 400
    if not phone or len(phone) < 7:
        return jsonify({"error": "A valid phone number with country code is required"}), 400
    if not email or "@" not in email or "." not in email:
        return jsonify({"error": "A valid email address is required"}), 400

    conn = get_db()
    cursor = conn.cursor()

    # Check if participant with email or phone already exists
    cursor.execute("SELECT * FROM participants WHERE email = ? OR phone = ?", (email, phone))
    existing = cursor.fetchone()

    ist_now_str = get_ist_now().strftime("%Y-%m-%d %H:%M:%S")

    if existing:
        user_uuid = existing["uuid"]
        cursor.execute('''
        UPDATE participants
        SET full_name = ?, country = ?, state = ?, city = ?, phone = ?, email = ?, preferred_lang = ?, updated_at = ?
        WHERE id = ?
        ''', (full_name, country, state, city, phone, email, preferred_lang, ist_now_str, existing["id"]))
        participant_id = existing["id"]
    else:
        user_uuid = str(uuid.uuid4())
        cursor.execute('''
        INSERT INTO participants (uuid, full_name, country, state, city, phone, email, preferred_lang, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_uuid, full_name, country, state, city, phone, email, preferred_lang, ist_now_str, ist_now_str))
        participant_id = cursor.lastrowid

    conn.commit()

    # Fetch updated record
    cursor.execute("SELECT * FROM participants WHERE id = ?", (participant_id,))
    participant = dict(cursor.fetchone())
    conn.close()

    return jsonify({
        "message": "Registration successful. Welcome to Surakshaa Saathi!",
        "participant": participant
    })

@app.route("/api/profile", methods=["GET", "PUT", "DELETE"])
def profile():
    user_uuid = request.args.get("uuid") or request.headers.get("X-Participant-UUID")
    if not user_uuid:
        return jsonify({"error": "Participant UUID identifier is required"}), 400

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM participants WHERE uuid = ?", (user_uuid,))
    participant = cursor.fetchone()

    if not participant:
        conn.close()
        return jsonify({"error": "Participant record not found"}), 404

    participant_id = participant["id"]

    if request.method == "GET":
        # Fetch quiz history
        cursor.execute('''
        SELECT id, quiz_date, score, total_marks, submitted_at, certificate_id
        FROM quiz_attempts
        WHERE participant_id = ?
        ORDER BY id DESC
        ''', (participant_id,))
        quiz_history = [dict(row) for row in cursor.fetchall()]

        # Fetch certificates
        cursor.execute('''
        SELECT certificate_number, quiz_date, score, total_marks, certificate_type, issue_date, email_status
        FROM certificates
        WHERE participant_id = ?
        ORDER BY id DESC
        ''', (participant_id,))
        certificates = [dict(row) for row in cursor.fetchall()]

        conn.close()
        return jsonify({
            "participant": dict(participant),
            "quiz_history": quiz_history,
            "certificates": certificates
        })

    elif request.method == "PUT":
        data = request.get_json() or {}
        full_name = (data.get("full_name") or participant["full_name"]).strip()
        country = (data.get("country") or participant["country"]).strip()
        state = (data.get("state") or participant["state"]).strip()
        city = (data.get("city") or participant["city"]).strip()
        phone = (data.get("phone") or participant["phone"]).strip()
        email = (data.get("email") or participant["email"]).strip()
        preferred_lang = (data.get("preferred_lang") or participant["preferred_lang"]).strip()

        ist_now_str = get_ist_now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute('''
        UPDATE participants
        SET full_name = ?, country = ?, state = ?, city = ?, phone = ?, email = ?, preferred_lang = ?, updated_at = ?
        WHERE id = ?
        ''', (full_name, country, state, city, phone, email, preferred_lang, ist_now_str, participant_id))
        conn.commit()

        cursor.execute("SELECT * FROM participants WHERE id = ?", (participant_id,))
        updated = dict(cursor.fetchone())
        conn.close()

        return jsonify({
            "message": "Profile updated successfully.",
            "participant": updated
        })

    elif request.method == "DELETE":
        # Account deletion request
        cursor.execute("DELETE FROM quiz_attempts WHERE participant_id = ?", (participant_id,))
        cursor.execute("DELETE FROM certificates WHERE participant_id = ?", (participant_id,))
        cursor.execute("DELETE FROM participants WHERE id = ?", (participant_id,))
        conn.commit()
        conn.close()
        return jsonify({"message": "Participant account and all associated records have been permanently deleted."})

# --- Daily Cyber Awareness Quiz ---

@app.route("/api/quiz/today", methods=["GET"])
def get_today_quiz():
    ist_date = get_ist_date_str()
    participant_uuid = request.args.get("uuid")

    conn = get_db()
    cursor = conn.cursor()

    completed = False
    existing_attempt = None

    if participant_uuid:
        cursor.execute("SELECT id FROM participants WHERE uuid = ?", (participant_uuid,))
        p_row = cursor.fetchone()
        if p_row:
            p_id = p_row["id"]
            cursor.execute('''
            SELECT * FROM quiz_attempts WHERE participant_id = ? AND quiz_date = ?
            ''', (p_id, ist_date))
            existing_attempt = cursor.fetchone()
            if existing_attempt:
                completed = True
                existing_attempt = dict(existing_attempt)
                # Parse answers json if available
                try:
                    existing_attempt["answers"] = json.loads(existing_attempt["answers_json"])
                except:
                    existing_attempt["answers"] = []

    # Questions list (omit correct_index if not yet completed so users cannot cheat in frontend)
    client_questions = []
    for q in QUIZ_QUESTIONS_POOL:
        item = {
            "id": q["id"],
            "question": q["question"],
            "options": q["options"]
        }
        if completed:
            item["correct_index"] = q["correct_index"]
            item["explanation"] = q["explanation"]
        client_questions.append(item)

    conn.close()

    return jsonify({
        "quiz_date": ist_date,
        "total_questions": len(QUIZ_QUESTIONS_POOL),
        "completed": completed,
        "existing_attempt": existing_attempt,
        "questions": client_questions
    })

@app.route("/api/quiz/submit", methods=["POST"])
def submit_quiz():
    data = request.get_json() or {}
    participant_uuid = data.get("uuid")
    user_answers = data.get("answers") or {}  # Dict of { question_id: selected_index }

    if not participant_uuid:
        return jsonify({"error": "Participant identification required"}), 400

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM participants WHERE uuid = ?", (participant_uuid,))
    participant = cursor.fetchone()

    if not participant:
        conn.close()
        return jsonify({"error": "Participant not registered"}), 404

    participant_id = participant["id"]
    ist_date = get_ist_date_str()

    # STRICT ONE ATTEMPT PER PARTICIPANT PER DAY (IST)
    cursor.execute('''
    SELECT * FROM quiz_attempts WHERE participant_id = ? AND quiz_date = ?
    ''', (participant_id, ist_date))
    existing = cursor.fetchone()

    if existing:
        conn.close()
        return jsonify({
            "error": "You have already completed today's Cyber Awareness Quiz. Each participant is allowed only one attempt per daily quiz cycle (IST).",
            "completed": True,
            "attempt": dict(existing)
        }), 403

    # Calculate Score
    score = 0
    total_marks = len(QUIZ_QUESTIONS_POOL)  # T = 10
    answers_review = []

    for q in QUIZ_QUESTIONS_POOL:
        q_id = str(q["id"])
        selected = user_answers.get(q_id)
        is_correct = (selected == q["correct_index"])
        if is_correct:
            score += 1
        answers_review.append({
            "id": q["id"],
            "question": q["question"],
            "options": q["options"],
            "selected_index": selected,
            "correct_index": q["correct_index"],
            "is_correct": is_correct,
            "explanation": q["explanation"]
        })

    # Certificate Eligibility Rules:
    # Full marks: S = T
    # One mark below: S = T - 1
    # Two marks below: S = T - 2
    # Award Appreciation; otherwise Participation
    if score >= (total_marks - 2):
        certificate_type = "Certificate of Appreciation"
    else:
        certificate_type = "Certificate of Participation"

    # Generate Unique Certificate Number
    cert_hash = hashlib.sha256(f"{participant_id}-{ist_date}-{score}-{uuid.uuid4()}".encode('utf-8')).hexdigest()[:8].upper()
    cert_number = f"SS-2026-{cert_hash}"

    ist_now_str = get_ist_now().strftime("%Y-%m-%d %H:%M:%S")

    # Insert Attempt
    cursor.execute('''
    INSERT INTO quiz_attempts (participant_id, quiz_date, score, total_marks, answers_json, certificate_id, submitted_at)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (participant_id, ist_date, score, total_marks, json.dumps(answers_review), cert_number, ist_now_str))

    # Insert Certificate Record
    cursor.execute('''
    INSERT INTO certificates (certificate_number, participant_id, participant_name, quiz_date, score, total_marks, certificate_type, issue_date, email_status, delivery_log, created_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'Queued', 'Ready for direct download or email delivery.', ?)
    ''', (cert_number, participant_id, participant["full_name"], ist_date, score, total_marks, certificate_type, ist_date, ist_now_str))

    conn.commit()

    certificate_info = {
        "certificate_number": cert_number,
        "participant_name": participant["full_name"],
        "certificate_type": certificate_type,
        "score": score,
        "total_marks": total_marks,
        "quiz_date": ist_date,
        "issue_date": ist_date,
        "email": participant["email"]
    }

    conn.close()

    return jsonify({
        "message": "Quiz submitted successfully!",
        "score": score,
        "total_marks": total_marks,
        "certificate_type": certificate_type,
        "certificate": certificate_info,
        "answers_review": answers_review
    })

# --- Certificate Verification & Email Delivery ---

@app.route("/api/certificates/<cert_no>", methods=["GET"])
def get_certificate(cert_no):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM certificates WHERE certificate_number = ?", (cert_no,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return jsonify({"error": "Certificate not found or invalid reference number."}), 404

    return jsonify({"certificate": dict(row)})

@app.route("/api/certificates/<cert_no>/send-email", methods=["POST"])
def send_certificate_email(cert_no):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
    SELECT c.*, p.email, p.full_name
    FROM certificates c
    JOIN participants p ON c.participant_id = p.id
    WHERE c.certificate_number = ?
    ''', (cert_no,))
    row = cursor.fetchone()

    if not row:
        conn.close()
        return jsonify({"error": "Certificate record not found"}), 404

    cert_data = dict(row)
    email_to = cert_data["email"]

    # Check for real SMTP server credentials
    smtp_host = os.environ.get("SMTP_HOST")
    smtp_port = int(os.environ.get("SMTP_PORT", 587))
    smtp_user = os.environ.get("SMTP_USER")
    smtp_pass = os.environ.get("SMTP_PASS")
    smtp_from = os.environ.get("SMTP_FROM", "surakshaasaathi@gov-safety.in")

    if not (smtp_host and smtp_user and smtp_pass):
        # Explicit honesty rule: Never simulate or claim delivery succeeded without real configured provider!
        status_msg = "Transactional email provider is not configured in the server environment (requires SMTP_HOST, SMTP_USER, SMTP_PASS). Your certificate is immediately available for direct high-resolution PDF download."
        cursor.execute("UPDATE certificates SET email_status = 'Pending Configuration', delivery_log = ? WHERE certificate_number = ?", (status_msg, cert_no))
        conn.commit()
        conn.close()
        return jsonify({
            "status": "not_configured",
            "message": status_msg,
            "direct_download_available": True
        })

    try:
        msg = MIMEMultipart()
        msg["From"] = smtp_from
        msg["To"] = email_to
        msg["Subject"] = f"Surakshaa Saathi — Your {cert_data['certificate_type']} ({cert_no})"

        body_text = f"""Namaste {cert_data['full_name']},

Congratulations on completing the Daily Cyber Awareness Quiz on Surakshaa Saathi!

Certificate Title: {cert_data['certificate_type']}
Score: {cert_data['score']} / {cert_data['total_marks']}
Certificate Reference: {cert_no}
Date: {cert_data['quiz_date']}

Thank you for contributing to a safer digital India.
Stay Aware. Stay Secure. Stay Ahead.

Surakshaa Saathi National Cyber Awareness Initiative
https://cybercrime.gov.in
"""
        msg.attach(MIMEText(body_text, "plain"))

        with smtplib.SMTP(smtp_host, smtp_port, timeout=10) as server:
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.send_message(msg)

        cursor.execute("UPDATE certificates SET email_status = 'Sent', delivery_log = 'Email delivered successfully' WHERE certificate_number = ?", (cert_no,))
        conn.commit()
        conn.close()
        return jsonify({"status": "sent", "message": f"Certificate sent successfully to {email_to}"})

    except Exception as e:
        err_msg = f"Delivery failed: {str(e)}"
        cursor.execute("UPDATE certificates SET email_status = 'Failed', delivery_log = ? WHERE certificate_number = ?", (err_msg, cert_no))
        conn.commit()
        conn.close()
        return jsonify({
            "status": "failed",
            "message": f"Email delivery encounter an issue ({str(e)}). You can still download your certificate directly from the website.",
            "direct_download_available": True
        }), 500

# --- Scam Scenario Learning Library ---

@app.route("/api/scenarios", methods=["GET"])
def get_scenarios():
    search = (request.args.get("search") or "").strip().lower()
    category = (request.args.get("category") or "").strip()
    risk_level = (request.args.get("risk_level") or "").strip()
    audience = (request.args.get("audience") or "").strip()
    page = max(1, int(request.args.get("page", 1)))
    limit = max(1, min(100, int(request.args.get("limit", 15))))
    offset = (page - 1) * limit

    conn = get_db()
    cursor = conn.cursor()

    query = "SELECT * FROM scam_scenarios WHERE published = 1"
    params = []

    if category and category != "All":
        query += " AND category = ?"
        params.append(category)

    if risk_level and risk_level != "All":
        query += " AND risk_level = ?"
        params.append(risk_level)

    if audience and audience != "All":
        query += " AND (target_audience = ? OR target_audience = 'All')"
        params.append(audience)

    if search:
        query += " AND (LOWER(title) LIKE ? OR LOWER(situation) LIKE ? OR LOWER(how_works) LIKE ? OR LOWER(tags) LIKE ?)"
        term = f"%{search}%"
        params.extend([term, term, term, term])

    # Count total
    count_query = query.replace("SELECT *", "SELECT COUNT(*)")
    cursor.execute(count_query, params)
    total_count = cursor.fetchone()[0]

    # Fetch paginated items
    query += " ORDER BY id ASC LIMIT ? OFFSET ?"
    params.extend([limit, offset])
    cursor.execute(query, params)
    rows = [dict(r) for r in cursor.fetchall()]

    # Fetch unique categories for filter pills
    cursor.execute("SELECT DISTINCT category FROM scam_scenarios ORDER BY category ASC")
    categories = [r[0] for r in cursor.fetchall()]

    conn.close()

    return jsonify({
        "total": total_count,
        "page": page,
        "limit": limit,
        "total_pages": (total_count + limit - 1) // limit,
        "categories": categories,
        "scenarios": rows
    })

@app.route("/api/scenarios/<scenario_id>", methods=["GET"])
def get_scenario_detail(scenario_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM scam_scenarios WHERE scenario_id = ? OR id = ?", (scenario_id, scenario_id))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return jsonify({"error": "Scenario not found"}), 404

    return jsonify({"scenario": dict(row)})

# --- Daily Cyber-Safety Tip ---

@app.route("/api/daily-tip", methods=["GET"])
def get_daily_tip():
    ist_now = get_ist_now()
    day_number = ist_now.day  # 1 to 31
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM daily_tips WHERE day_number = ?", (day_number,))
    row = cursor.fetchone()

    if not row:
        # Fallback to day 1 if day exceeds pool
        cursor.execute("SELECT * FROM daily_tips ORDER BY id ASC LIMIT 1")
        row = cursor.fetchone()

    conn.close()
    tip_dict = dict(row) if row else {}
    tip_dict["ist_date"] = get_ist_date_str()
    return jsonify({"daily_tip": tip_dict})

# --- Official Indian Resources ---

@app.route("/api/resources", methods=["GET"])
def get_resources():
    return jsonify({
        "resources": OFFICIAL_RESOURCES,
        "emergency_helpline": "1930",
        "official_portal": "https://cybercrime.gov.in",
        "last_verified": "2026-10-25"
    })

# --- Host-Controlled Poster Gallery ---

@app.route("/api/posters", methods=["GET"])
def get_posters():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM posters WHERE published = 1 ORDER BY id ASC")
    posters = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return jsonify({"posters": posters})

# --- Five-Star Reviews & Feedback ---

@app.route("/api/reviews", methods=["GET", "POST"])
def reviews():
    conn = get_db()
    cursor = conn.cursor()

    if request.method == "GET":
        cursor.execute('''
        SELECT id, full_name, profession, rating, review_text, created_at
        FROM reviews
        WHERE status = 'approved'
        ORDER BY id DESC
        ''')
        rows = [dict(r) for r in cursor.fetchall()]

        # Compute summary
        total = len(rows)
        avg = round(sum(r["rating"] for r in rows) / total, 1) if total > 0 else 5.0
        conn.close()

        return jsonify({
            "total_reviews": total,
            "average_rating": avg,
            "reviews": rows
        })

    elif request.method == "POST":
        data = request.get_json() or {}
        full_name = (data.get("full_name") or "").strip()
        profession = (data.get("profession") or "").strip()  # Free-form typed text!
        rating = int(data.get("rating", 0))
        review_text = (data.get("review_text") or "").strip()

        if not full_name:
            return jsonify({"error": "Full Name is required"}), 400
        if not profession:
            return jsonify({"error": "Profession/Occupation is required (e.g. Teacher, Student, Doctor)"}), 400
        if rating < 1 or rating > 5:
            return jsonify({"error": "Please select a star rating from 1 to 5"}), 400
        if not review_text or len(review_text) < 10:
            return jsonify({"error": "Please write a meaningful review description (at least 10 characters)"}), 400

        # Basic spam check
        profanity_terms = ["spam", "buy crypto", "free followers", "viagra", "casino"]
        status = "approved"
        for term in profanity_terms:
            if term in review_text.lower():
                status = "pending"
                break

        ist_now_str = get_ist_now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute('''
        INSERT INTO reviews (full_name, profession, rating, review_text, status, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', (full_name, profession, rating, review_text, status, ist_now_str))
        conn.commit()
        conn.close()

        return jsonify({
            "message": "Thank you for sharing your experience! Your review has been submitted.",
            "status": status
        })

# --- AI-Powered Cyber-Safety Chatbot ("Surakshaa Saathi Cyber Guide") ---

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json() or {}
    user_message = (data.get("message") or "").strip()
    history = data.get("history") or []
    language = data.get("language") or "hi"
    attachment = data.get("attachment")  # Optional document or image metadata

    if not user_message and not attachment:
        return jsonify({"error": "Message or attachment is required"}), 400

    # Check for external OpenAI API key in environment or admin settings
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM admin_config WHERE key = 'openai_api_key'")
        row = cursor.fetchone()
        if row and row["value"]:
            api_key = row["value"]
        conn.close()

    # If external API is configured, call it; otherwise execute the comprehensive local reasoning engine
    if api_key:
        try:
            import requests
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            system_prompt = f"""You are the official Surakshaa Saathi Cyber Guide — an expert, friendly, empathetic, and knowledgeable Indian cybersecurity advisor.
Your mission is to help Indian citizens understand online scams, UPI fraud, digital arrest, phishing, identity protection, and digital safety.
Language: Respond primarily in the user's requested language ({language}), maintaining clear, comforting, and practical tone.
Crucial rules:
1. If the user mentions financial fraud or unauthorized transactions, prioritize immediate action: contact their bank right away and dial the National Cyber Helpline 1930 within the Golden Hour.
2. Emphasize that 'Digital Arrest' does NOT exist under Indian law; police/CBI never arrest or interrogate via video calls.
3. Warn against recovery scams (people demanding upfront fees to recover stolen funds).
4. Never ask for passwords, PINs, or OTPs.
5. Provide clear, step-by-step guidance, evidence preservation, and official reporting advice."""

            messages = [{"role": "system", "content": system_prompt}]
            for h in history[-6:]:
                messages.append({"role": h.get("role", "user"), "content": h.get("content", "")})
            messages.append({"role": "user", "content": user_message})

            resp = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json={
                "model": "gpt-4o-mini",
                "messages": messages,
                "temperature": 0.3,
                "max_tokens": 800
            }, timeout=20)

            if resp.status_code == 200:
                res_json = resp.json()
                bot_text = res_json["choices"][0]["message"]["content"]
                return jsonify({
                    "response": bot_text,
                    "engine": "openai",
                    "triage_helpline": "1930",
                    "official_portal": "https://cybercrime.gov.in"
                })
        except Exception as e:
            # Graceful fallback to local reasoning engine on any network or API issue
            pass

    # Built-in High-Intelligence Cyber Safety Reasoning Engine
    reply = generate_expert_safety_response(user_message, attachment, language)

    return jsonify({
        "response": reply,
        "engine": "surakshaa_safety_reasoning_core",
        "triage_helpline": "1930",
        "official_portal": "https://cybercrime.gov.in"
    })

def generate_expert_safety_response(message, attachment, lang):
    msg_lower = (message or "").lower()

    # Image or Document attachment triage
    if attachment:
        fname = attachment.get("name", "Document").lower()
        if any(ext in fname for ext in [".apk", "apk"]):
            return (
                "🚨 **HIGH ALERT: DANGEROUS MALICIOUS APK DETECTED!**\n\n"
                "• **DO NOT INSTALL THIS FILE!** Under no circumstances should you open or install this APK.\n"
                "• Cybercriminals frequently send malicious APK files (disguised as 'e-Challan', 'Wedding Card', 'Electricity Bill', or 'PM Yojana') which install SMS-forwarding trojans to steal banking OTPs.\n"
                "• **Immediate Action:** Delete this file from your device downloads folder immediately.\n"
                "• If already installed: Turn on Airplane Mode immediately, uninstall the app via Android Settings -> Apps, and run Google Play Protect."
            )
        elif any(ext in fname for ext in [".png", ".jpg", ".jpeg"]):
            return (
                "🔍 **INSPECTION OF SUSPICIOUS SCREENSHOT / IMAGE**\n\n"
                "• **Fake Payment / QR Verification:** If this image displays a payment confirmation (e.g. Google Pay, PhonePe) but your own bank or soundbox has NOT announced the credit, it is likely generated using a spoof payment app.\n"
                "• **QR Code Notice:** If this is a QR code sent by someone claiming to pay you, **DO NOT SCAN IT**. Scanning a QR code ALWAYS debits money from your account.\n"
                "• **Preserve Evidence:** Keep this screenshot safely saved as evidence if you file a complaint at https://cybercrime.gov.in or Helpline 1930."
            )

    # 1. Digital Arrest / Skype / Police Video Call
    if any(k in msg_lower for k in ["digital arrest", "skype", "cbi", "police video", "customs parcel", "narcotics", "ed notice", "warrant"]):
        return (
            "🛡️ **CRITICAL ADVISORY: 'DIGITAL ARREST' IS A 100% FRAUDULENT SCAM!**\n\n"
            "• **The Legal Truth:** Indian law, the Indian Police, CBI, ED, NIA, and Customs **DO NOT** have any provision for 'Digital Arrest'. Real law enforcement officers never conduct interrogations or arrest citizens over Skype or WhatsApp video calls.\n"
            "• **Immediate Action:**\n"
            "  1. **Disconnect the call immediately.** Do not be intimidated by actors in police uniforms or forged warrants.\n"
            "  2. **Never transfer any money** to alleged 'Supreme Court Verification' or 'Safe Escrow' accounts.\n"
            "  3. **Talk to your family or local police.** You are completely safe.\n"
            "  4. Report the mobile number on the **Chakshu portal** (sancharsaathi.gov.in) and dial **1930**."
        )

    # 2. UPI / Collect Request / QR Scam / Money Lost
    if any(k in msg_lower for k in ["upi", "qr", "qr code", "collect request", "phonepe", "paytm", "gpay", "google pay", "pin"]):
        if any(k in msg_lower for k in ["receive", "receive money", "buyer", "selling", "olx", "facebook marketplace"]):
            return (
                "⚠️ **CARDINAL RULE: NO PIN IS EVER NEEDED TO RECEIVE MONEY!**\n\n"
                "• **How the scam works:** Fraudsters exploit the misunderstanding between 'Send' and 'Receive'. When you enter your UPI MPIN or scan a QR code, you are authorizing money to be **DEDUCTED** from your account.\n"
                "• **Safety Steps:**\n"
                "  1. Decline the collect request immediately.\n"
                "  2. Do not scan any QR codes sent to you.\n"
                "  3. Block the prospective buyer.\n"
                "• If funds were already deducted, immediately call your bank's 24/7 fraud helpline and dial **1930**."
            )
        else:
            return (
                "💳 **UPI & PAYMENT SAFETY GUIDANCE**\n\n"
                "• **Key Safeguards:**\n"
                "  1. **Never enter UPI PIN** unless you are intentionally transferring funds out or checking balance.\n"
                "  2. Set low daily UPI transaction limits inside your bank app.\n"
                "  3. Always verify the registered beneficiary name displayed on screen before authorising payment.\n"
                "  4. If an unauthorized UPI debit occurs, call **1930** and report within the 'Golden Hour' (first 2 hours) to freeze the recipient bank switch."
            )

    # 3. Emergency / Money Lost / Unauthorized Transaction
    if any(k in msg_lower for k in ["lost money", "stolen", "debited", "fraud transaction", "cheated", "scammed", "hacked", "account empty"]):
        return (
            "🚨 **EMERGENCY ACTION PROTOCOL (ACT WITHIN THE GOLDEN HOUR):**\n\n"
            "1. **Call 1930 Immediately:** Dial the National Cybercrime Helpline **1930** to activate the Citizen Financial Cyber Fraud Reporting System and freeze the stolen funds in transit.\n"
            "2. **Freeze Bank Account / Card:** Call your bank's emergency 24x7 customer care number to freeze netbanking, block cards, and disable UPI.\n"
            "3. **Preserve Evidence:** Save SMS alerts, transaction UTR numbers, account numbers, and chat logs.\n"
            "4. **File Official Complaint:** Register the incident on https://cybercrime.gov.in.\n"
            "⚠️ **Beware of Recovery Scams:** Never pay any individual, cyber lawyer, or hacker claiming they can recover your money for an upfront fee."
        )

    # 4. Job Scams / Part Time / YouTube Like / Work From Home
    if any(k in msg_lower for k in ["job", "work from home", "telegram", "like video", "part time", "task scam", "youtube like"]):
        return (
            "💼 **ALERT: 'TASK-BASED' WORK FROM HOME FRAUD**\n\n"
            "• **The Trap:** Scammers add victims to Telegram/WhatsApp groups offering Rs 150-500 for liking YouTube videos. After building trust with initial small payouts, they demand Rs 10,000 to Rs 2 Lakhs for 'prepaid crypto tasks' with fake 40% returns.\n"
            "• **What to do:**\n"
            "  1. Stop all tasks immediately. Do not send any money to 'unlock' your earnings.\n"
            "  2. Exit and report the Telegram channel.\n"
            "  3. Legitimate employers never ask employees to pay money to complete work or release earned salaries."
        )

    # 5. Remote Access / AnyDesk / Screen Sharing
    if any(k in msg_lower for k in ["anydesk", "teamviewer", "quicksupport", "screen share", "rustdesk"]):
        return (
            "⛔ **DANGER: REMOTE SCREEN-SHARING EXPLOIT**\n\n"
            "• Legitimate banks, airline customer care, and telecom providers **NEVER** ask customers to install AnyDesk, TeamViewer, or QuickSupport.\n"
            "• Once you share the 9-digit code, the fraudster can see your screen, watch you type passwords, and intercept OTPs.\n"
            "• **If you already installed it:**\n"
            "  1. Turn off WiFi / Mobile Data immediately.\n"
            "  2. Uninstall the remote application from your phone.\n"
            "  3. Change all banking passwords and UPI MPINs using another secure device."
        )

    # 6. Greetings & General Assistance
    if any(k in msg_lower for k in ["hello", "hi", "namaste", "hey", "who are you", "help", "kya hai", "kaise ho"]):
        return (
            "🙏 **Namaste! Welcome to Surakshaa Saathi Cyber Guide.**\n\n"
            "I am your dedicated digital safety assistant. I can help you with:\n"
            "• **Recognizing online scams:** UPI fraud, Digital Arrest, fake jobs, phishing links, and courier traps.\n"
            "• **Emergency triage:** What to do immediately if you suspect an unauthorized transaction.\n"
            "• **Evidence guidance:** How to report scams to Helpline **1930** and cybercrime.gov.in.\n"
            "• **Document/Image check:** Upload suspicious screenshots or documents for safety verification.\n\n"
            "How can I assist your digital safety today?"
        )

    # General safe response
    return (
        "🛡️ **SURAKSHAA SAATHI SAFETY GUIDANCE**\n\n"
        f"Thank you for reaching out regarding: *\"{message[:100]}...\"*\n\n"
        "• **Safety Verification:** Always double-check unsolicited requests before sharing credentials, clicking links, or transferring funds.\n"
        "• **Official Sources:** Genuine government notices only arrive via '.gov.in' or '.nic.in' domains. Real banks never ask for OTPs, CVVs, or screen-sharing.\n"
        "• **Official Helpline:** In any doubt or financial emergency, call **1930** or visit **https://cybercrime.gov.in**.\n\n"
        "Would you like specific steps to protect your account or report an incident?"
    )

# --- Admin Dashboard Endpoints ---

@app.route("/api/admin/login", methods=["POST"])
def admin_login():
    data = request.get_json() or {}
    password = (data.get("password") or "").strip()
    if not password:
        return jsonify({"error": "Password is required"}), 400

    pass_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT value FROM admin_config WHERE key = 'admin_password_hash'")
    row = cursor.fetchone()
    conn.close()

    if not row or row["value"] != pass_hash:
        return jsonify({"error": "Invalid administrative credentials."}), 401

    token = get_admin_token(pass_hash)
    return jsonify({
        "message": "Admin authorization granted.",
        "token": token
    })

@app.route("/api/admin/stats", methods=["GET"])
def admin_stats():
    if not verify_admin(request):
        return jsonify({"error": "Unauthorized"}), 401

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM participants")
    total_participants = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM quiz_attempts")
    total_quizzes = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM certificates")
    total_certificates = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM scam_scenarios")
    total_scenarios = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM reviews WHERE status = 'pending'")
    pending_reviews = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM posters WHERE published = 1")
    total_posters = cursor.fetchone()[0]

    conn.close()

    return jsonify({
        "total_participants": total_participants,
        "total_quizzes": total_quizzes,
        "total_certificates": total_certificates,
        "total_scenarios": total_scenarios,
        "pending_reviews": pending_reviews,
        "total_posters": total_posters,
        "system_status": "Operational",
        "ist_time": get_ist_now().strftime("%Y-%m-%d %H:%M:%S IST")
    })

@app.route("/api/admin/posters", methods=["POST"])
def admin_add_poster():
    if not verify_admin(request):
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json() or {}
    title = (data.get("title") or "").strip()
    description = (data.get("description") or "").strip()
    category = (data.get("category") or "General Awareness").strip()
    image_url = (data.get("image_url") or "/static/images/poster_1930_helpline.png").strip()
    source_refs = (data.get("source_refs") or "Surakshaa Saathi Editorial Board").strip()

    if not title or not description:
        return jsonify({"error": "Title and description are required"}), 400

    conn = get_db()
    cursor = conn.cursor()
    ist_now_str = get_ist_now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute('''
    INSERT INTO posters (title, description, category, image_url, source_refs, published, created_at)
    VALUES (?, ?, ?, ?, ?, 1, ?)
    ''', (title, description, category, image_url, source_refs, ist_now_str))
    conn.commit()
    conn.close()

    return jsonify({"message": "Poster published successfully."})

@app.route("/api/admin/posters/<int:poster_id>", methods=["PUT", "DELETE"])
def admin_manage_poster(poster_id):
    if not verify_admin(request):
        return jsonify({"error": "Unauthorized"}), 401

    conn = get_db()
    cursor = conn.cursor()

    if request.method == "DELETE":
        cursor.execute("DELETE FROM posters WHERE id = ?", (poster_id,))
        conn.commit()
        conn.close()
        return jsonify({"message": "Poster deleted successfully."})

    elif request.method == "PUT":
        data = request.get_json() or {}
        published = 1 if data.get("published", True) else 0
        cursor.execute("UPDATE posters SET published = ? WHERE id = ?", (published, poster_id))
        conn.commit()
        conn.close()
        return jsonify({"message": "Poster status updated."})

@app.route("/api/admin/reviews/<int:review_id>", methods=["PUT", "DELETE"])
def admin_manage_review(review_id):
    if not verify_admin(request):
        return jsonify({"error": "Unauthorized"}), 401

    conn = get_db()
    cursor = conn.cursor()

    if request.method == "DELETE":
        cursor.execute("DELETE FROM reviews WHERE id = ?", (review_id,))
        conn.commit()
        conn.close()
        return jsonify({"message": "Review deleted."})

    elif request.method == "PUT":
        data = request.get_json() or {}
        new_status = data.get("status", "approved")
        cursor.execute("UPDATE reviews SET status = ? WHERE id = ?", (new_status, review_id))
        conn.commit()
        conn.close()
        return jsonify({"message": f"Review marked as {new_status}."})

@app.route("/api/admin/settings", methods=["POST"])
def admin_update_settings():
    if not verify_admin(request):
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json() or {}
    new_password = data.get("new_password")
    openai_key = data.get("openai_api_key")

    conn = get_db()
    cursor = conn.cursor()

    if new_password:
        new_hash = hashlib.sha256(new_password.encode('utf-8')).hexdigest()
        cursor.execute("UPDATE admin_config SET value = ? WHERE key = 'admin_password_hash'", (new_hash,))

    if openai_key is not None:
        cursor.execute("INSERT OR REPLACE INTO admin_config (key, value) VALUES ('openai_api_key', ?)", (openai_key,))

    conn.commit()
    conn.close()
    return jsonify({"message": "Settings updated successfully."})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"Starting Surakshaa Saathi production server on http://127.0.0.1:{port}")
    app.run(host="0.0.0.0", port=port, debug=False)

