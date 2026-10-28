import json
import os
import sqlite3
from database import get_db, init_db

QUIZ_QUESTIONS_POOL = [
    {
        "id": 1,
        "question": "Which of the following is true when receiving money via UPI on apps like Google Pay, PhonePe, or Paytm?",
        "options": [
            "You must enter your 4 or 6-digit UPI MPIN to receive the funds",
            "No UPI PIN or password is ever required to receive money into your account",
            "You need to scan a QR code sent by the payer to credit your account",
            "You must share your debit card CVV number with the sender"
        ],
        "correct_index": 1,
        "explanation": "UPI PIN is solely used for authorizing DEBITS (sending money or checking balance). Under no circumstances is a PIN or QR scan required to receive funds. Any request asking for a PIN to receive money is an absolute scam."
    },
    {
        "id": 2,
        "question": "What is the official Indian National Cyber Crime Helpline number for immediate reporting of financial cyber fraud within the 'Golden Hour'?",
        "options": [
            "100",
            "1930",
            "1098",
            "1800"
        ],
        "correct_index": 1,
        "explanation": "Helpline 1930 is the designated citizen financial cyber fraud reporting helpline managed by the Ministry of Home Affairs (MHA) and Indian Cyber Crime Coordination Centre (I4C). Calling 1930 promptly helps freeze funds before scammers cash out."
    },
    {
        "id": 3,
        "question": "An unknown caller claims to be a Police Officer on Skype, stating that illegal narcotics were seized in a parcel under your Aadhaar and places you under 'Digital Arrest'. What is the legal reality?",
        "options": [
            "Digital Arrest is an official expedited legal procedure permitted under the Code of Criminal Procedure",
            "There is no provision for 'Digital Arrest' in Indian law; police or CBI never conduct arrests or demand money over Skype/WhatsApp video calls",
            "You must remain on video call until you transfer security bond money to the officer's verification account",
            "Only the Enforcement Directorate (ED) has the power to place citizens under Digital Arrest"
        ],
        "correct_index": 1,
        "explanation": "Indian law and law enforcement agencies (Police, CBI, ED, Customs, NIA) DO NOT recognize any concept of 'Digital Arrest'. No law enforcement officer conducts virtual arrests, interrogations, or demands money transfers via video calls. This is a severe criminal intimidation scam."
    },
    {
        "id": 4,
        "question": "A buyer on an online marketplace insists on sending you money via a QR code and asks you to scan it in your payment app. What will happen if you scan it and enter your PIN?",
        "options": [
            "The advance amount will be immediately credited to your bank account",
            "Money will be debited from your bank account and transferred to the scammer",
            "The marketplace will hold the funds in safe escrow",
            "Your bank account will receive a verification token"
        ],
        "correct_index": 1,
        "explanation": "Scanning a QR code in a payment app is an action to PAY money, not to receive it. Entering your MPIN authorizes an outgoing debit transaction from your bank account."
    },
    {
        "id": 5,
        "question": "How can you protect your Aadhaar card from being misused for unauthorized SIM card issuances or micro-ATM (AePS) cash withdrawals?",
        "options": [
            "Laminate the physical Aadhaar card with plastic",
            "Use 'Masked Aadhaar' showing only the last 4 digits, and enable 'Biometric Lock' on the UIDAI portal/mAadhaar app",
            "Write your phone number in permanent ink across the card",
            "Share the full 12 digits only over WhatsApp voice calls"
        ],
        "correct_index": 1,
        "explanation": "UIDAI provides the 'Masked Aadhaar' option (which conceals the first 8 digits) for public identity verification, and the 'Biometric Lock' feature in the mAadhaar app to prevent rogue fingerprint extraction and unauthorized AePS withdrawals."
    },
    {
        "id": 6,
        "question": "A caller claiming to represent your bank asks you to download 'AnyDesk', 'TeamViewer', or 'QuickSupport' to fix an online banking issue. What should you do?",
        "options": [
            "Download it immediately so they can fix your phone remotely",
            "Provide the 9-digit session code shown on your screen",
            "Hang up immediately; legitimate banks never ask customers to install remote access or screen-sharing software",
            "Transfer Rs 10 to test the connection"
        ],
        "correct_index": 2,
        "explanation": "Screen sharing and remote access apps give fraudsters complete control to view your screen, intercept SMS OTPs, and observe you typing passwords and PINs. Bank representatives are strictly forbidden from asking customers to install remote desktop utilities."
    },
    {
        "id": 7,
        "question": "You receive an SMS: 'Your electricity power will be disconnected at 9:30 PM due to unpaid bill. Call 9876543210 immediately'. What is the safest way to verify?",
        "options": [
            "Call the 10-digit mobile number given in the SMS right away",
            "Log in directly to your official state electricity board portal or check your bill on an authorized Bharat BillPay (BBPS) app",
            "Download the recharge APK sent by the officer over WhatsApp",
            "Pay Rs 100 on the link provided in the SMS"
        ],
        "correct_index": 1,
        "explanation": "Power distribution companies (DISCOMs) never send personal 10-digit phone numbers or threaten disconnections on a 1-hour notice via SMS. Always check consumer accounts directly through official state DISCOM portals or BBPS-enabled banking apps."
    },
    {
        "id": 8,
        "question": "What is a 'Recovery Scam' that frequently targets victims who have already lost money in cyber fraud?",
        "options": [
            "An insurance policy that automatically recovers stolen cryptocurrency",
            "A secondary fraud where scammers impersonate cyber lawyers or white-hat hackers demanding upfront fees to 'recover' previously lost funds",
            "An automated RBI tool to reverse UPI transactions",
            "A police department compensation scheme"
        ],
        "correct_index": 1,
        "explanation": "Recovery scams prey on desperate victims by promising 100% retrieval of lost money or cryptocurrency in exchange for advance 'legal fees', 'hacker retainers', or 'tax payments'. Once paid, the recovery agents disappear."
    },
    {
        "id": 9,
        "question": "Which domain extension indicates an authentic, verified Indian Central or State Government department website?",
        "options": [
            ".gov.in or .nic.in",
            ".org.in or .co.in",
            ".government-india.com",
            ".gov-secure.info"
        ],
        "correct_index": 0,
        "explanation": "All legitimate Indian government departments, ministries, courts, and enforcement agencies are strictly hosted on '.gov.in' or '.nic.in' domains managed by the National Informatics Centre (NIC). Private commercial extensions like .com, .top, or .xyz are never used for official government portals."
    },
    {
        "id": 10,
        "question": "If you suspect an unauthorized transaction has occurred on your bank account or credit card, what is the single most critical first step?",
        "options": [
            "Post about it on Instagram and wait for customer replies",
            "Immediately contact your bank's 24x7 fraud prevention helpline to freeze the account/card and dial 1930",
            "Wait 48 hours for the transaction to automatically reconcile",
            "Contact a private detective found on social media"
        ],
        "correct_index": 1,
        "explanation": "Reporting unauthorized transactions immediately to your bank limits customer liability under RBI mandates and allows the bank to block further leakages. Simultaneously calling 1930 activates the National Cyber Crime inter-bank freeze protocol."
    }
]

DAILY_TIPS_POOL = [
    {
        "day": 1,
        "title": "The Golden Rule of UPI",
        "tip": "UPI PIN is only used for sending money or checking your balance. You NEVER need to enter a PIN, password, or scan a QR code to receive money.",
        "explanation": "If someone claims they are sending you money and instructs you to type your UPI PIN or scan a QR code, they are trying to debit your account.",
        "topic": "Banking and UPI"
    },
    {
        "day": 2,
        "title": "Beware of 'Digital Arrest' Threats",
        "tip": "There is NO provision for 'Digital Arrest' in Indian law. Police, CBI, ED, or Customs never arrest or interrogate citizens over Skype or WhatsApp video calls.",
        "explanation": "If an unknown caller in uniform demands money or orders you to stay on video call, disconnect immediately, block the number, and dial 1930.",
        "topic": "Digital Arrest"
    },
    {
        "day": 3,
        "title": "Act in the 'Golden Hour'",
        "tip": "Report any unauthorized financial transaction immediately to Helpline 1930 and your bank within 2 hours.",
        "explanation": "Speed is crucial. The I4C 1930 mechanism alerts bank nodes to freeze stolen money before fraudsters withdraw it from ATMs or purchase crypto.",
        "topic": "Emergency Guidance"
    },
    {
        "day": 4,
        "title": "Lock Your Aadhaar Biometrics",
        "tip": "Prevent fraudulent micro-ATM (AePS) cash withdrawals by enabling 'Biometric Lock' in the UIDAI mAadhaar app.",
        "explanation": "When biometrics are locked, no one can withdraw money using your fingerprint until you momentarily unlock it yourself.",
        "topic": "Identity Theft"
    },
    {
        "day": 5,
        "title": "Never Install Remote Access Apps",
        "tip": "Never install AnyDesk, TeamViewer, or QuickSupport at the instruction of an unknown caller or search engine customer care number.",
        "explanation": "Remote access apps let criminals view your screen, record your passwords, and steal OTPs in real time.",
        "topic": "Remote Access"
    },
    {
        "day": 6,
        "title": "Verify Links Before Clicking",
        "tip": "Inspect the URL carefully. Official Indian government websites strictly end with .gov.in or .nic.in, never .com, .xyz, or .top.",
        "explanation": "Phishing sites copy the exact design of banks and government portals. Always verify the domain name in your browser's address bar.",
        "topic": "Phishing"
    },
    {
        "day": 7,
        "title": "The Dangers of 'Part-Time Task' Scams",
        "tip": "Beware of Telegram and WhatsApp messages offering high daily pay for liking YouTube videos or rating Google Maps locations.",
        "explanation": "They start by paying Rs 200 to gain your trust, then trap you in 'VIP prepaid tasks' requiring lakhs in non-refundable deposits.",
        "topic": "Job Scams"
    },
    {
        "day": 8,
        "title": "Beware of Fake Soundboxes & QR Scams",
        "tip": "Merchants should never rely on customer phone screenshots for payment confirmation. Always verify audio announcements from your soundbox.",
        "explanation": "Spoof payment generator apps simulate fake payment success animations with custom merchant names and amounts.",
        "topic": "Merchant Safety"
    },
    {
        "day": 9,
        "title": "Protect Elderly Family Members",
        "tip": "Warn senior citizens against late-night SMS threats claiming power or water disconnections.",
        "explanation": "Utility boards never send 1-hour disconnection warnings from personal 10-digit mobile numbers.",
        "topic": "Senior Safety"
    },
    {
        "day": 10,
        "title": "Guard Your SIM Card",
        "tip": "Never dial *21* or unfamiliar USSD codes suggested by callers claiming to fix poor cellular reception.",
        "explanation": "These codes set up unconditional call forwarding, routing your bank verification calls directly to the scammer's phone.",
        "topic": "Mobile Safety"
    }
]

OFFICIAL_RESOURCES = [
    {
        "name": "National Cyber Crime Reporting Portal",
        "purpose": "Central portal of the Government of India for reporting all types of cybercrimes, including financial frauds, identity theft, and crimes against women and children.",
        "contact": "Toll Free Helpline: 1930",
        "website": "https://cybercrime.gov.in/",
        "guidance": "File complaint promptly. Provide transaction ID, UTR number, bank statement, screenshot, and sender mobile number.",
        "verified_date": "2026-10-20"
    },
    {
        "name": "Citizen Financial Cyber Fraud Reporting System (1930)",
        "purpose": "National 24x7 emergency helpline operational under the Indian Cyber Crime Coordination Centre (I4C), Ministry of Home Affairs.",
        "contact": "Dial 1930 (Toll Free across India)",
        "website": "https://cybercrime.gov.in/",
        "guidance": "Call within the 'Golden Hour' (first 2 hours of unauthorized transaction) to freeze money in banking transit nodes.",
        "verified_date": "2026-10-20"
    },
    {
        "name": "CERT-In (Indian Computer Emergency Response Team)",
        "purpose": "National nodal agency under MeitY for responding to computer security incidents, ransomware attacks, malware alerts, and vulnerability advisories.",
        "contact": "Incident Hotline: 1800-11-4949 | Email: incident@cert-in.org.in",
        "website": "https://www.cert-in.org.in/",
        "guidance": "Report phishing URLs, malware outbreaks, ransomware incidents, and critical data breaches.",
        "verified_date": "2026-10-18"
    },
    {
        "name": "Reserve Bank of India (RBI) Ombudsman & Sachet",
        "purpose": "Apex monetary authority overseeing banking fraud regulations, customer compensation, unauthorized debit liabilities, and reporting unauthorized NBFCs.",
        "contact": "RBI Integrated Ombudsman Portal (Toll Free: 14448)",
        "website": "https://cms.rbi.org.in/ | https://sachet.rbi.org.in/",
        "guidance": "If your bank fails to resolve an unauthorized transaction dispute within 30 days, escalate to the RBI Integrated Ombudsman.",
        "verified_date": "2026-10-18"
    },
    {
        "name": "National Consumer Helpline (NCH)",
        "purpose": "Official portal of the Ministry of Consumer Affairs for addressing e-commerce frauds, fake goods delivery, refund refusals, and service deficiencies.",
        "contact": "Helpline: 1915 | SMS: 8800001915",
        "website": "https://consumerhelpline.gov.in/",
        "guidance": "Register grievances against registered and unregistered e-commerce companies for counterfeit or undelivered merchandise.",
        "verified_date": "2026-10-15"
    },
    {
        "name": "Sanchar Saathi & Chakshu (Department of Telecommunications)",
        "purpose": "Government of India initiative to report suspect fraud communications, track and block lost/stolen mobile phones, and check SIM cards linked to your name.",
        "contact": "Website: sancharsaathi.gov.in",
        "website": "https://sancharsaathi.gov.in/",
        "guidance": "Use 'Chakshu' facility to report fraudulent calls/SMS received on your phone, and 'TAFCOP' to inspect SIM cards registered under your Aadhaar.",
        "verified_date": "2026-10-22"
    }
]

SEED_POSTERS = [
    {
        "title": "National Cyber Helpline 1930 — Act in the Golden Hour",
        "description": "Official national cybersecurity awareness poster illustrating the urgent protocol for freezing stolen funds within 2 hours of unauthorized bank or UPI transactions.",
        "category": "Helpline & Emergency",
        "image_url": "/static/images/poster_1930_helpline.png",
        "source_refs": "Ministry of Home Affairs (MHA) & I4C Guidelines"
    },
    {
        "title": "QR Code Truth: QR is strictly for PAYING, Never for Receiving",
        "description": "Essential citizen defense poster dismantling the reverse QR scam. Clarifies that no PIN or scan is ever required to receive funds into any bank account.",
        "category": "UPI & Payment Safety",
        "image_url": "/static/images/poster_qr_truth.png",
        "source_refs": "NPCI UPI Safety Awareness Protocol"
    },
    {
        "title": "Digital Arrest is 100% FAKE — Real Police Never Arrest on Skype",
        "description": "High-impact advisory warning citizens against fake police video calls, forged arrest warrants, and intimidation by fake CBI/ED officers over WhatsApp.",
        "category": "Digital Arrest Defense",
        "image_url": "/static/images/poster_digital_arrest.png",
        "source_refs": "CERT-In Cyber Advisory & State Cyber Police Bulletins"
    },
    {
        "title": "5 Golden Rules of Safe Online Banking",
        "description": "Comprehensive visual guide on strong passwords, biometric locking, masked Aadhaar usage, disabling unnecessary international card limits, and ignoring unverified links.",
        "category": "Digital Hygiene",
        "image_url": "/static/images/poster_banking_rules.png",
        "source_refs": "Reserve Bank of India (RBI) Kehta Hai Campaign"
    },
    {
        "title": "Senior Cyber Guard — Protecting Elders from Utility & Call Scams",
        "description": "Specially designed for senior citizens and families to identify late-evening power disconnection threats, grandchild emergency bail scams, and fake pension updates.",
        "category": "Senior Citizen Protection",
        "image_url": "/static/images/poster_senior_safety.png",
        "source_refs": "National Commission for Senior Citizens & I4C"
    },
    {
        "title": "Student Scam Alert: The Trap of Leaked Papers & Task Scams",
        "description": "Educating youth and college students against Telegram leaked question paper rackets, work-from-home video liking tasks, and predatory loan app blackmail.",
        "category": "Student Cyber Awareness",
        "image_url": "/static/images/poster_student_safety.png",
        "source_refs": "UGC Anti-Cyber Harassment & Cyber Dost Guidelines"
    }
]

SEED_REVIEWS = [
    {
        "full_name": "Dr. Rajeshwar Sharma",
        "profession": "Senior High School Principal",
        "rating": 5,
        "review_text": "Surakshaa Saathi is an outstanding national asset! We organized a school-wide cyber awareness drive where 800+ students took the Daily Quiz and received their Certificates of Appreciation. The scenario library explains scams in clear, defensible language without fear-mongering."
    },
    {
        "full_name": "Priyanka Nambiar",
        "profession": "Software Engineer & Parent",
        "rating": 5,
        "review_text": "The 13 Indian languages support is genuinely impressive. My mother was able to read all safety tips and scam breakdowns in Malayalam with complete clarity. The explanation of the Digital Arrest scam saved our family from severe anxiety."
    },
    {
        "full_name": "Col. Vikramjit Singh (Retd.)",
        "profession": "Retired Army Officer & Resident Welfare President",
        "rating": 5,
        "review_text": "A remarkably polished, trustworthy platform. The poster gallery provided high-resolution printable graphics that we installed on our society notice boards. The daily IST quiz keeps our senior citizens alert and updated on modern cyber hazards."
    },
    {
        "full_name": "Ananya Sengupta",
        "profession": "College Student & Aspiring Designer",
        "rating": 5,
        "review_text": "The 3D interactive background, smooth navigation, and the AI Cyber Guide are world-class! The chatbot accurately guided me through a suspicious job offer scam on Telegram and explained how to verify corporate domains."
    },
    {
        "full_name": "Mohammed Farooq",
        "profession": "Small Retail Business Owner",
        "rating": 5,
        "review_text": "As a shopkeeper, the merchant QR tampering and fake payment screenshot scenarios were eye-openers. I trained my counter staff immediately. The instant certificate generation is also very motivating."
    }
]

def seed_all_supporting_data():
    conn = get_db()
    cursor = conn.cursor()

    # Seed tips
    cursor.execute("DELETE FROM daily_tips")
    for tip in DAILY_TIPS_POOL:
        cursor.execute('''
        INSERT INTO daily_tips (day_number, title, tip_text, explanation, related_topic)
        VALUES (?, ?, ?, ?, ?)
        ''', (tip["day"], tip["title"], tip["tip"], tip["explanation"], tip["topic"]))

    # Seed posters
    cursor.execute("DELETE FROM posters")
    for p in SEED_POSTERS:
        cursor.execute('''
        INSERT INTO posters (title, description, category, image_url, source_refs, published, created_at)
        VALUES (?, ?, ?, ?, ?, 1, datetime('now'))
        ''', (p["title"], p["description"], p["category"], p["image_url"], p["source_refs"]))

    # Seed reviews
    cursor.execute("DELETE FROM reviews")
    for r in SEED_REVIEWS:
        cursor.execute('''
        INSERT INTO reviews (full_name, profession, rating, review_text, status, created_at)
        VALUES (?, ?, ?, ?, 'approved', datetime('now'))
        ''', (r["full_name"], r["profession"], r["rating"], r["review_text"]))

    conn.commit()
    conn.close()
    print("Supporting data (Daily Tips, Posters, Reviews) successfully seeded!")

if __name__ == "__main__":
    init_db()
    seed_all_supporting_data()

