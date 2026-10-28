import json
import os
import sqlite3
from database import get_db

def create_scenario_item(sc_id, title, cat, risk, aud, sit, works, signs, manip, vict_do, avoid, reduce, report, tags):
    return {
        "scenario_id": f"SCN-{sc_id:04d}",
        "title": title,
        "category": cat,
        "risk_level": risk,
        "target_audience": aud,
        "situation": sit,
        "how_works": works,
        "warning_signs": signs,
        "manipulation": manip,
        "victim_actions": vict_do,
        "avoid_actions": avoid,
        "risk_reduction": reduce,
        "reporting_guidance": report,
        "last_reviewed": "2026-10-15",
        "tags": tags
    }

def get_complete_scenarios_list():
    scenarios = []

    def add(title, cat, risk, aud, sit, works, signs, manip, vict_do, avoid, reduce, report, tags):
        sc_id = len(scenarios) + 1
        scenarios.append(create_scenario_item(sc_id, title, cat, risk, aud, sit, works, signs, manip, vict_do, avoid, reduce, report, tags))

    # --- 1. Banking and UPI (1-15) ---
    add("Reverse UPI 'Collect Request' Refund Scam", "Banking and UPI", "Critical", "All",
        "A user selling furniture online receives a call from a buyer who promises to pay via UPI. Instead of sending money, the buyer sends a UPI 'Collect Request' for Rs 15,000, claiming the seller must approve it to receive the advance.",
        "Fraudsters exploit the misunderstanding between 'Send' and 'Receive' in UPI apps. They initiate a debit collect request. If the victim enters their UPI MPIN, money is debited immediately from their account.",
        "Receiving a request that asks for your UPI PIN; caller repeatedly saying 'Enter PIN to accept money'; urgency and pressure on call.",
        "Confusion of technical terms, claiming bank policy requires PIN verification for receiving merchant transfers.",
        "Decline the collect request immediately; block the caller; check account statement; notify bank if clicked.",
        "Never enter your UPI PIN to receive money under any circumstances. UPI PIN is solely for authorising debits.",
        "Remember the cardinal rule: 'No PIN is required to receive money in UPI'. Set daily transaction limits.",
        "Report caller on National Cyber Crime Portal (cybercrime.gov.in) and call 1930 within the golden hour.",
        "UPI, Collect Request, MPIN, Online Selling")

    add("Screen Sharing App Remote UPI Theft (AnyDesk/TeamViewer)", "Banking and UPI", "Critical", "Seniors",
        "A bank customer facing failed transaction issues calls a number found online. The 'executive' instructs them to install QuickSupport or AnyDesk to resolve the pending refund.",
        "The fraudster asks the victim to read out the 9-digit remote access code. Once connected, they watch the victim open their banking app and type their credentials and MPIN, capturing full screen contents and session tokens.",
        "Request to install remote desktop utilities (AnyDesk, TeamViewer, RustDesk); asking for 9-digit session code.",
        "Fake empathy, official sounding jargon ('diagnostic verification', 'screen mirror protocol').",
        "Disconnect internet immediately, uninstall the remote tool, change netbanking and UPI passwords from another phone.",
        "Do not allow screen sharing with unknown persons; never open banking apps while a remote session is running.",
        "Do not search for customer care numbers on public search engines; only use official bank apps or physical passbook.",
        "Call bank customer care to freeze accounts, report to cybercrime.gov.in and dial 1930.",
        "Remote Access, AnyDesk, Screen Share, UPI Theft")

    add("Fake Payment Confirmation Screenshot Scam", "Banking and UPI", "High", "Professionals",
        "A shopkeeper is shown a realistic-looking Google Pay/PhonePe screenshot on the customer's phone showing 'Rs 4,500 Paid Successfully'. The customer rushes away before the merchant's soundbox confirms payment.",
        "Fraudsters use spoof payment generator apps that simulate transaction success screens with animated ticks, fake UTR numbers, and merchant names, while no actual bank transfer occurs.",
        "No SMS confirmation received on merchant phone; Soundbox did not announce payment; customer is overly impatient.",
        "Creating artificial hurry, claiming network lag on merchant's phone, feigning distress or bus schedule urgency.",
        "Do not release goods until your own soundbox or bank SMS/app registers the credit. Note vehicle/person details.",
        "Never accept visual phone screenshots as proof of funds transfer.",
        "Rely exclusively on audio soundbox notifications or direct SMS from your banking provider.",
        "Report the fake transaction attempt to local police cyber cell and market association.",
        "Fake Screenshot, Spoof UPI, Soundbox, Retail Scam")

    add("Overpayment and Return via UPI Trap", "Banking and UPI", "High", "Citizens",
        "A person receives an SMS claiming Rs 50,000 has been accidentally credited to their bank account by a stranger. Moments later, a weeping caller begs for Rs 45,000 to be returned immediately for medical treatment.",
        "The scammer sends a spoofed SMS styled like a bank notification, or uses a stolen bank account to initiate a fraudulent transfer that will soon be reversed by the real victim's bank, leaving the second victim with a net loss.",
        "SMS originates from a random 10-digit mobile number rather than an official bank sender ID (e.g., AD-HDFCBK); immediate emotional phone call.",
        "Emotional manipulation, invoking medical emergencies, dying relatives, or severe panic.",
        "Log into your bank app independently to check true account balance; do not refund any money directly; ask caller to contact their bank.",
        "Never refund disputed funds directly via UPI. Tell the caller to initiate an official bank-to-bank reversal.",
        "Educate family members on checking official bank statements rather than relying on SMS alerts alone.",
        "Inform your bank branch manager in writing about the unverified credit and notify 1930.",
        "Overpayment, Accidental Transfer, Social Engineering, UPI")

    add("SIM Swap Attack on Netbanking Authentication", "Banking and UPI", "Critical", "Professionals",
        "A user suddenly notices 'No Service' on their mobile network. Within an hour, multiple unauthorized IMPS transfers drain their savings account while they struggle to get signal.",
        "Scammers obtain the victim's personal details and ID copy, file a fraudulent SIM replacement with the telecom provider, and gain access to the physical number to receive SMS OTPs for banking resets.",
        "Sudden, unexplained loss of mobile network signal; multiple missed calls from unknown foreign numbers preceding signal loss.",
        "Distracting the victim with nuisance calls so they turn off their phone or ignore network disappearance.",
        "Immediately contact telecom provider from another phone to report unauthorized SIM swap; contact bank to lock netbanking.",
        "Do not ignore unexpected loss of cellular service, especially if netbanking credentials were recently compromised.",
        "Upgrade to telecom e-SIM with PIN protection; register email-based secondary alerts with your bank.",
        "Dial 1930 immediately to freeze transactions in the banking switch before fraudsters cash out.",
        "SIM Swap, Netbanking, OTP Interception, Telecom")

    add("Credit Card Limit Enhancement Phishing Call", "Banking and UPI", "High", "Citizens",
        "A caller impersonating the bank's credit card department offers a free upgrade to 'Platinum Card' with double credit limit and zero annual fee, asking the customer to confirm the 16-digit card number and CVV.",
        "The scammer uses leaked card databases to quote partial details, building false trust, then asks for expiry date, CVV, and the OTP sent by the bank, which is actually authorizing an international e-commerce purchase.",
        "Caller asking for CVV, card expiry date, or OTP; promises of miraculous free limit upgrades without formal application.",
        "False authority, claiming the offer expires at midnight or is a special loyalty reward.",
        "Refuse to provide CVV or OTP; disconnect the call; open the official bank mobile application to manage card limits securely.",
        "Never disclose CVV, card PIN, or transaction OTP to anyone, including bank representatives.",
        "Enable transaction limits, disable international usage, and turn off contactless payments when not in use.",
        "Block the card immediately using the bank mobile app and report the incident to 1930.",
        "Credit Card, CVV, Limit Upgrade, Phishing")

    add("Cashback Scratch Card Phishing Links", "Banking and UPI", "Medium", "Students",
        "A student receives a WhatsApp link: 'Congratulations! You won Rs 1,850 PhonePe festival cashback. Tap to claim directly to bank account'.",
        "The link directs to a web page mimicking Google Pay or Paytm with a digital scratch card. Upon scratching, it opens the user's UPI app with an autofilled payment request to a scammer's VPA.",
        "Web links promising unconditional cashback or lottery; redirects to UPI apps asking to 'Pay' or 'Authorise'.",
        "Gamification (scratching cards, spinning wheels) triggering quick dopamine and reduced caution.",
        "Close the webpage immediately; do not interact with any autofilled UPI prompt; report the sender on WhatsApp.",
        "Do not click on unverified cashback links shared on messaging platforms or social media.",
        "Remember legitimate cashbacks are credited automatically to your linked account without visiting external links.",
        "Report the phishing URL to CERT-In (cert-in.org.in) and WhatsApp anti-abuse.",
        "Cashback, Scratch Card, Phishing, UPI")

    add("Unclaimed Fixed Deposit & Dormant Account Fraud", "Banking and UPI", "High", "Seniors",
        "A senior citizen receives a phone call from an alleged 'RBI nodal officer' stating their deceased parent's dormant fixed deposit worth Rs 8 Lakhs has been traced and requires Rs 12,000 stamp duty fee to release.",
        "Fraudsters research public obituaries or leaked banking records, claiming unclaimed funds exist, demanding upfront processing fees, affidavits, or transfer taxes.",
        "Demand for upfront fees via UPI or personal accounts to release government or bank inheritance money.",
        "Appealing to sentimental family ties and unexpected windfall wealth.",
        "Do not transfer any money. Visit the physical bank branch where the deceased held accounts; verify via RBI UDGAM portal.",
        "Never pay upfront fees to claim dormant accounts or legitimate bank funds.",
        "Use RBI's official UDGAM portal (udgam.rbi.org.in) to search for unclaimed deposits safely.",
        "Report fraud attempts to the local police cyber cell and cybercrime.gov.in.",
        "Dormant Account, Senior Citizen, UDGAM, Fixed Deposit")

    add("FASTag Expiry and Low Balance Scam SMS", "Banking and UPI", "Medium", "Citizens",
        "A car owner receives an SMS: 'Your FASTag account will be blacklisted within 24 hours due to KYC incompletion. Update now: http://fastag-kyc-update.top'.",
        "The URL leads to a spoofed NHAI / bank portal that asks the victim to enter their mobile number, vehicle number, and UPI credentials, extracting money under the guise of a Rs 10 verification charge.",
        "SMS containing urgent threat of FASTag suspension; suspicious non-government domain extensions (.top, .info, .xyz).",
        "Threat of disruption to highway travel, toll fines, and urgent 24-hour deadlines.",
        "Delete the SMS; check FASTag balance directly inside your authorized bank app or My FASTag official NHAI app.",
        "Never update FASTag KYC through links received via SMS or WhatsApp.",
        "Keep FASTag linked to official wallets with limited balances rather than primary bank accounts.",
        "Report fraudulent SMS to Chakshu portal (sancharsaathi.gov.in) and cybercrime.gov.in.",
        "FASTag, KYC, Phishing, Highway Toll")

    add("Electricity Bill Disconnection Threat SMS", "Banking and UPI", "High", "Seniors",
        "An SMS arrives at 8 PM: 'Dear customer, your electricity will be disconnected tonight at 9:30 PM due to unpaid previous month bill. Contact power officer at 9876543210 immediately.'",
        "When the anxious victim calls, the fraudster impersonates an electricity board official, claiming system error, and asks them to download a Rs 10 recharge APK or open a payment link, resulting in device compromise.",
        "Late evening SMS threatening immediate power cut; personal 10-digit mobile number provided for customer support.",
        "Instilling fear of darkness, food spoiling in refrigerators, or inconvenience for family.",
        "Do not call the mobile number. Check electricity bill status on official state electricity distribution portal or consumer bill.",
        "Do not download any APK files sent via WhatsApp or SMS to resolve utility bills.",
        "Official electricity disconnections are never executed through personal mobile numbers on 1-hour notice without written prior notices.",
        "Report the mobile number on Sanchar Saathi's Chakshu portal and dial 1930.",
        "Electricity Bill, Disconnection, Utility Scam, APK Malware")

    add("ATM Card Skimming and Shimming", "Banking and UPI", "High", "All",
        "A customer uses an ATM kiosk at a quiet location. Two days later, unauthorized cash withdrawals take place across another state.",
        "Criminals install thin magnetic stripe skimmers or microchip shimmers in the ATM card slot, paired with a hidden pinhole camera or fake keypad overlay to record the ATM PIN.",
        "Loose or unusually bulky card reader bezel; misaligned keypad; glue residue around ATM card slot.",
        "Targeting poorly lit, unguarded standalone ATM booths during holiday weekends.",
        "Cover the keypad with your free hand while typing PIN; report suspicious ATM machines to bank security immediately.",
        "Do not use ATMs where the card reader seems loose, damaged, or exhibits blinking lights of odd colors.",
        "Prefer bank branch on-site ATMs; switch to contactless cash withdrawal via UPI at supported ATMs.",
        "Call bank customer support immediately to block ATM card and dispute fraudulent withdrawals.",
        "ATM Skimming, Shimming, PIN Theft, Banking")

    add("Fake Income Tax Refund Phishing SMS", "Banking and UPI", "High", "Professionals",
        "During tax season, a taxpayer gets an SMS: 'Your Income Tax Refund of Rs 24,490 has been approved. Submit your bank account details here to receive within 2 hours: http://incometax-efiling-refund.in'.",
        "The phishing website replicates the Income Tax e-Filing portal, prompting the user for PAN, Aadhaar, Netbanking login credentials, and card details, which are harvested instantly.",
        "Refund amount ending in odd numbers to look genuine; shortened or unofficial domain names; SMS from private phone numbers.",
        "Greed and excitement of getting a tax refund from the government.",
        "Do not click the link. Log in directly to the official Income Tax portal (incometax.gov.in) to check refund status.",
        "Never submit netbanking passwords or debit card details to receive any government refund.",
        "Income Tax department always credits refunds directly to pre-validated bank accounts without external third-party links.",
        "Forward phishing SMS to incident@cert-in.org.in and webmanager@incometax.gov.in.",
        "Income Tax, Tax Refund, Phishing, Government Impersonation")

    add("Pre-Approved Loan Processing Fee Scam", "Banking and UPI", "High", "Citizens",
        "A person receives an SMS or WhatsApp message: 'Pre-approved loan of Rs 5,00,000 at 2% interest. No income proof required. Pay Rs 2,500 file processing charge to disburse.'",
        "The scammer sends fake loan sanction letters with forged RBI or bank logos. Once the victim pays the initial processing fee, new demands emerge for GST, insurance, and clearance fees until the victim stops paying.",
        "Unrealistic low interest rates without credit verification; demanding upfront processing fees into personal savings accounts.",
        "Exploiting urgent financial distress, medical debt, or poor credit scores.",
        "Stop all communication; do not transfer any processing fees; demand physical branch verification.",
        "Never pay upfront fees to secure a loan. Legitimate financial institutions deduct processing fees from disbursed amounts.",
        "Verify all lenders on the RBI List of Registered NBFCs and Banks before engaging.",
        "Lodge an official complaint with the local cybercrime cell and at cybercrime.gov.in.",
        "Pre-Approved Loan, Processing Fee, Advance Fee, Fraud")

    add("Biometric AePS (Aadhaar Enabled Payment System) Skimming", "Banking and UPI", "Critical", "Citizens",
        "A rural resident discovers that funds were withdrawn from their bank account through AePS without their knowledge, even though their ATM card and phone were in their pocket.",
        "Criminals acquire cloned silicone fingerprint replicas obtained from registry offices or property documents, using them on AePS micro-ATMs to withdraw cash up to daily limits.",
        "Unauthorized SMS alerts showing AePS cash withdrawal; no physical card or OTP was requested.",
        "Exploiting trusting citizens who frequently leave thumb impressions on public deeds or unverified kiosks.",
        "Immediately open the UIDAI mAadhaar app or website and 'Lock Biometrics' feature to prevent further AePS debits.",
        "Do not leave unprotected photocopies of Aadhaar cards with full numbers visible; use Masked Aadhaar.",
        "Keep biometric lock enabled in the UIDAI portal; unlock only momentarily when you personally need to authenticate.",
        "Lodge an urgent complaint with your bank's fraud monitoring cell and report to 1930.",
        "AePS, Aadhaar, Biometric Skimming, UIDAI")

    add("Cheque Kiting and Positive Pay System Evasion", "Banking and UPI", "High", "Professionals",
        "A business owner writes a vendor cheque of Rs 15,000. Scammers intercept the physical cheque in transit, use chemical wash to alter payee name and amount to Rs 4,50,000, and present it for clearing.",
        "Chemical alteration of physical cheques to change beneficiary details and amounts, targeting high balance business accounts.",
        "Discrepancies in monthly bank statement; clearing alerts for unexpected high amounts.",
        "Exploiting delays in physical delivery and non-utilization of bank safety mandates.",
        "Immediately notify bank branch manager to recall clearing; file police FIR for cheque interception and forgery.",
        "Never issue high-value cheques without registering details in the bank's Positive Pay System (PPS).",
        "Use permanent indelible ink; write 'A/C Payee' clearly; register Positive Pay details with your bank for any cheque above Rs 50,000.",
        "File complaint with bank grievance redressal officer and local economic offences wing.",
        "Cheque Forgery, Positive Pay, Chemical Wash, Business Scam")

    # --- Categories generator to reach 265 unique scenarios ---
    categories_matrix = [
        ("QR-code and Payment Fraud", 12, [
            ("Merchant Counter QR Code Replacement Scam", "Fraudsters walk into busy shops, placing fraudulent printed stickers over the merchant's original standee to divert payments."),
            ("Reverse QR 'Receive Money' Scam", "Scammers send a QR code image claiming that scanning it deposits an advance payment, whereas scanning always debits money."),
            ("Parking Meter Fake QR Code Sticker Phishing", "Attackers paste fake QR stickers on municipal parking signs leading to phishing portals that steal card details."),
            ("Restaurant Table Menu QR Code Hijack", "Replacing tabletop ordering QR codes with fake links that collect bill payments directly to rogue accounts."),
            ("Electricity Bill Printed QR Phishing Overlay", "Pasting counterfeit QR stickers over physical paper utility bills delivered to apartment mailboxes."),
            ("Temple Donation Box Counterfeit QR Code", "Affixing unauthorized QR stickers on donation boxes at crowded shrines to divert religious offerings."),
            ("Petrol Pump Attendant Swapped QR Device", "Rogue attendants carrying unauthorized personal QR cards claiming dispenser network timeouts."),
            ("E-Challan Fake QR on Traffic Violation Notice", "Fake paper violation slips on car windshields with QR codes leading to phishing payment gateways."),
            ("Charity Relief Campaign Fake QR on Social Media", "Stolen disaster photos paired with personal UPI QR codes running on sponsored social campaigns."),
            ("Event Ticket Entry Gate Counterfeit QR Swap", "Selling duplicated QR ticket barcodes outside stadiums and concert halls."),
            ("WiFi Hotspot 'Scan QR to Connect & Authenticate'", "Malicious QR codes in transit hubs harvesting email credentials under guise of free WiFi."),
            ("Courier Return Package Barcode Tampering", "Rogue delivery executives scanning fake pickup codes to misdirect valuable returns.")
        ]),
        ("Phishing and Fake Websites", 15, [
            ("Bank Netbanking Domain Typosquatting Portal", "Registering lookalike domain names with copied bank designs to capture credentials."),
            ("Income Tax e-Filing Notice Phishing Email", "Spoofed tax notice emails threatening 48-hour penalties to trick taxpayers into fake portals."),
            ("Fake EPFO Portal PF Withdrawal Scam", "Bogus portals mimicking EPFO harvesting UAN login credentials to re-route savings."),
            ("Google Search Sponsored Ad Phishing for Customer Care", "Purchasing sponsored ads on search engines to place fake helpline numbers at top results."),
            ("Fake Government PM-Kisan Yojana Portal", "Luring rural farmers with promises of bonus installments to harvest bank details."),
            ("Fake University Online Degree Portal", "Counterfeit distance learning websites selling unaccredited bogus degrees."),
            ("Fake Scholarship Portal for Underprivileged Students", "Charging non-existent registration fees for fake national scholarship grants."),
            ("Fake Visa and Immigration Embassy Portal", "Cloned embassy visa portals charging fake biometric appointment fees."),
            ("Fake Stock Exchange & Demat Account Portal", "Imposter web trading terminals directing stock funds into criminal mule accounts."),
            ("Fake Hotel and Resort Booking Website", "Boutique hotel cloned sites demanding 100% advance payments during peak holiday seasons."),
            ("Phishing for Netflix / OTT Subscription Suspended", "Spoofed billing emails threatening account cancellation to harvest credit cards."),
            ("Fake Matrimonial Identity and Extortion", "Customs parcel clearance scam targeting singles on matrimonial websites."),
            ("Fake Anti-Virus Renewal Pop-Up Scam", "Browser locking audio alerts coercing users to call fake tech support call centers."),
            ("Counterfeit E-Commerce Festive Season Sale", "Instagram flash sale ads offering 90% discounts with fake non-delivering storefronts."),
            ("Fake Vehicle Insurance Policy Renewal Scam", "Issuing counterfeit PDF vehicle insurance policies that leave motorists legally unprotected.")
        ]),
        ("Social Media Scams", 15, [
            ("Instagram Influencer Brand Ambassadorship Scam", "Charging aspiring creators upfront shipping fees for non-existent luxury merchandise sponsorships."),
            ("Compromised Friend WhatsApp Distress Scam", "Hijacking WhatsApp accounts and blasting contact lists with urgent emergency medical money requests."),
            ("Deepfake Video Call Sextortion Blackmail", "Recording victim faces during brief video calls to morph explicit pornography for extortion."),
            ("Telegram Work-from-Home Video Liking Scam", "Promising daily payouts for liking YouTube videos, then locking victims into prepaid VIP tasks."),
            ("Fake Celebrity Giveaway on Facebook / YouTube", "Looping celebrity interview footage in live streams demanding token entry fees to win prizes."),
            ("Fake NGO Animal Rescue Donation Scam", "Stealing emotional animal rescue footage from foreign shelters paired with domestic UPI handles."),
            ("Fake Dating App Blackmail (Honeytrap)", "Luring dating app users into private compromising video calls for extortion."),
            ("Facebook Marketplace Bogus Buyer Army Officer Scam", "Posing as defense personnel using forged military IDs and demanding QR code payment verification."),
            ("Hacked Instagram Account Recovery Fee Scam", "Bogus white-hat hackers charging upfront fees to recover stolen social media accounts."),
            ("Fake Copyright Infringement Notice Phishing", "Phishing direct messages threatening account deletion to steal credentials and 2FA codes."),
            ("Compromised LinkedIn Profile Job Offer Scam", "Sending executable infostealers disguised as job descriptions and NDAs from hijacked HR accounts."),
            ("Fake Viral WhatsApp Audio Rumour & Panic", "Spreading alarming voice notes regarding public contamination to drive ad traffic."),
            ("Fake Giveaways for WhatsApp Gold & Free Internet", "Chain viral links promising free 5G data that force sharing to multiple WhatsApp groups."),
            ("Fake Paid Collaboration with Brand Scam", "Sending malicious video editing tools that hijack YouTube creator channels."),
            ("Social Media Polling Phishing Link Trap", "Competitions requiring WhatsApp Web QR scanning to cast votes, hijacking sessions.")
        ]),
        ("Online Shopping", 14, [
            ("Unbelievable 90% Discount Luxury Watch Trap", "Delivering cheap plastic dummies while advertising authentic Swiss watches at 95% off."),
            ("Cash on Delivery (COD) Empty Box Courier Scam", "Dispatching unrequested cheap parcels to households relying on confusing family orders."),
            ("Fake Return Pickup Courier Charge Trap", "Impersonating logistics agents to charge non-existent refund pickup fees via UPI."),
            ("Non-Delivery of High-Value Electronics on Bogus Portal", "Setting up short-lived hardware webstores taking direct NEFT payments and disappearing."),
            ("Bait and Switch Mobile Phone Courier Trap", "Packing bricks of matching weight in authentic courier shipments on peer-to-peer classifieds."),
            ("Fake Flipkart Big Billion Day Lucky Draw Spin Wheel", "Rigged digital spin wheels convincing every participant they won high-end phones for delivery fees."),
            ("Duplicate E-Commerce Invoice for Paid Order Scam", "Intercepting order details to send fake invoices claiming primary payments failed."),
            ("Social Media Boutique Saree / Dress Non-Delivery", "Purchasing bot followers on Instagram boutiques to collect advance UPI payments and block buyers."),
            ("Fake Medicines and Health Supplements Portal", "Selling counterfeit or contaminated prescription medications without doctor verification."),
            ("Liquor Home Delivery Advance Payment Trap", "Poisoning Google Maps listings for local wine shops to extract upfront UPI delivery charges."),
            ("Fake Pet Sale and Pet Transport Deposit Fraud", "Using stolen puppy photos to extract successive pet transport crate and insurance fees."),
            ("Furniture Rental Advance Security Deposit Theft", "Offering discounted appliance rentals to steal deposits without delivering furniture."),
            ("Pre-Order Gaming Console / Gadget Scalping Scam", "Pretending to hold scarce gaming consoles on Telegram taking full non-refundable pre-orders."),
            ("Fake Automotive Spare Parts Website Scam", "Scraping auto repair forums to sell non-existent obsolete car components to desperate owners.")
        ]),
        ("Investment and Cryptocurrency", 16, [
            ("Telegram High-Yield Crypto Trading Bot Scam", "Simulating fake algorithmic trading yields and demanding endless withdrawal liquidity fees."),
            ("Pig Butchering (Sha Zhu Pan) Romance Investment Trap", "Building long-term romantic rapport before introducing victims to rigged foreign forex platforms."),
            ("Fake IPO Allotment and Pre-IPO Institutional Shares Trap", "Impersonating investment banks in WhatsApp groups promising guaranteed allotments in hot IPOs."),
            ("Ponzi Multi-Level Marketing (MLM) Pyramid Scheme", "Structuring investment returns strictly around recruiting downstream members until collapse."),
            ("Fake Stock Market WhatsApp Tip Channel Scam", "Broadcasting contradictory stock calls to sub-groups to sell overpriced fraudulent VIP channels."),
            ("Cryptocurrency Cloud Mining Contract Fraud", "Selling non-existent cloud hashrate contracts operating as classic Ponzi schemes."),
            ("Pump and Dump Penny Stock Manipulation Ring", "Blasting bulk SMS tips to dump illiquid penny stocks onto trapped retail investors."),
            ("Fake Commodity and Gold Trading Terminal", "Virtual closed-book trading software manipulating spreads to trigger forced margin liquidations."),
            ("NFT (Non-Fungible Token) Rug Pull Scam", "Collecting digital asset mint funds for hyped roadmaps before deleting Discord channels."),
            ("Fake Peer-to-Peer (P2P) Crypto Arbitrage Loop", "Promising risk-free arbitrage on obscure foreign exchanges that freeze deposits."),
            ("Binary Options 60-Second Bet Scam", "Rigged 60-second binary outcome mobile apps operating as illegal gambling rings."),
            ("Fake Carbon Credit / Green Energy Investment", "Selling bogus certified green carbon credits with fabricated land titles and environmental yields."),
            ("Fake Pre-IPO Startup Equity Secondary Market", "Forging share transfer deeds for unlisted unicorn tech companies."),
            ("Deepfake Video Elon Musk / Ambani Crypto Doubler", "Using AI-synthesized videos of famous leaders announcing fake crypto doubling addresses."),
            ("Bank Account Mule Recruitment for Crypto Laundering", "Paying students to route illicit cryptocurrency proceeds through their personal savings accounts."),
            ("DeFi Liquidity Pool Phishing Smart Contract Trap", "Deceptive smart contract approvals requesting unlimited token allowances to drain wallets.")
        ]),
        ("Employment and Job Offers", 15, [
            ("Part-Time YouTube Video Liking Scam", "Paying small initial bonuses for watching videos before requiring large prepaid investment tasks."),
            ("Fake Dubai Oil & Gas Overseas Job Offer", "Sending lavish overseas employment contracts demanding medical checkup and visa processing fees."),
            ("Data Entry Security Deposit Refund Trap", "Demanding refundable security deposits for offline typing work with impossible error quotas."),
            ("Freelance Upwork Escrow Bypass Theft", "Coercing freelancers off-platform to avoid fees, then taking delivered work without payment."),
            ("Amazon Product Reviewer Advance Fee Scam", "Promising high reviewer commissions on condition of buying expensive products on third-party links."),
            ("Aviation Cabin Crew Training Academy Fraud", "Operating fake airline interview rounds that demand mandatory paid uniform and grooming courses."),
            ("Medical Transcription Work from Home Trap", "Selling overpriced training software and refusing transcriptions on fabricated accuracy flaws."),
            ("Fake Railway Recruitment Board (RRB) Exam Scam", "Selling forged appointment letters for government railway vacancies for lakhs in cash."),
            ("Cruise Ship Hospitality Job Visa Trap", "Targeting hospitality workers with fake maritime placement permits and seaman book fees."),
            ("Captive Call Center Placement Fee Scam", "Charging recruitment training fees with false guarantees of placement in multinational BPOs."),
            ("Online Translation Project Deposit Fraud", "Extracting translation security deposits and disappearing once the translated manuscript is submitted."),
            ("Content Writing Paid Assessment Trap", "Requiring applicants to complete unpaid 'assessment articles' that are published without hiring."),
            ("Hotel Management Internship in Europe Scam", "Selling fake Schengen J-1 hospitality internship visas to culinary students."),
            ("Digital Marketing Apprentice Stipend Withholding", "Exploiting college interns for free social media labor under false promises of permanent jobs."),
            ("Envelope Packing Home Cottage Industry Trap", "Selling raw materials at inflated rates and refusing to buy back finished packaged goods.")
        ]),
        ("Loan and Financial Services", 14, [
            ("Predatory Instant Loan App Contact Blackmail", "Apps harvesting complete phonebooks and photos to harass contacts with vulgar morphed photos upon 7-day default."),
            ("Fake CIBIL Score Repair Guarantee Scam", "Promising to illegally delete loan default records from credit bureaus for advance consultancy fees."),
            ("Unsecured Business Loan Processing Advance Fee", "Forging SME loan sanction letters to extract GST, stamp duty, and legal inspection fees."),
            ("Government Subsidy PMEGP Loan Approval Trap", "Charging commission to fast-track Prime Minister Employment Generation Programme subsidies."),
            ("Fake Collateral Property Loan Sanction Fraud", "Demanding property valuation fees for non-existent low-interest real estate mortgages."),
            ("Microfinance Group Loan Identity Hijack", "Collecting village women's Aadhaar cards to take unauthorized group loans from micro-lenders."),
            ("Low Interest Home Loan Balance Transfer Scam", "Offering fake 4% interest rates to trick homeowners into signing predatory third-party promissory notes."),
            ("Forged Bank NOC Certificate for Cleared Loan", "Selling fake No Objection Certificates that leave borrowers with unclosed active debts in bureau records."),
            ("Agricultural Tractor Loan Subsidy Scam", "Targeting farmers with fake Central tractor purchase subsidy schemes requiring advance token deposits."),
            ("Fake Education Loan Disbursement Advance Fee", "Exploiting desperate students with fake foreign university education loan clearance charges."),
            ("Vehicle Hypothecation Removal Extortion", "RTO agents charging bribes to clear vehicle hypothecations while filing counterfeit clearance documents."),
            ("Gold Loan Valuation Swap Pawnshop Fraud", "Substituting genuine pawned gold jewelry with brass duplicates inside unorganized loan shops."),
            ("Peer-to-Peer Lending High Return Default Trap", "Unregulated P2P portals fabricating borrower creditworthiness while founders siphon deposited capital."),
            ("Credit Card Debt Consolidation Advance Fee", "Promising to settle credit card debt at 50% discount in exchange for upfront legal retainer fees.")
        ]),
        ("Identity Theft", 12, [
            ("Aadhaar Number Leak for Fraudulent SIM Cards", "Using leaked photocopies of Aadhaar cards to activate SIM cards issued to cybercriminal syndicates."),
            ("Stolen PAN Card Used for Bogus Loan Disbursements", "Acquiring credit lines on instant digital lending apps using leaked PAN numbers of unsuspecting citizens."),
            ("Synthetic Identity Creation Using Stolen Voter ID", "Combining legitimate voter card numbers with fabricated names to create synthetic ghost identities."),
            ("Fake Corporate Directorship Registered with Stolen DIN", "Registering shell companies with the Ministry of Corporate Affairs using stolen Director Identification Numbers."),
            ("Passport Data Leak for International Sim Cards", "Selling stolen passport scans on dark web forums to register roaming SIM cards for transnational fraud."),
            ("Rented Apartment Electricity Bill Used for Fake Bank Account", "Tenant utility bills used by unauthorized parties to open fraudulent current bank accounts."),
            ("Stolen Driving License Used for Car Rental Thefts", "Renting luxury self-drive vehicles using stolen driver licenses and absconding with stripped vehicles."),
            ("College Degree Certificate Misuse for Corporate Impersonation", "Forging candidate resumes with real alumni registration numbers to pass corporate background checks."),
            ("Masked Aadhaar Verification Bypass Scam", "Tricking citizens into providing unmasked physical Aadhaar cards for routine hotel or gym check-ins."),
            ("Salary Slip and Bank Statement Forgery Ring", "Syndicates forging PDF bank statements and salary slips to commit large-scale mortgage fraud."),
            ("Biometric Fingerprint Trace on Land Registry Deeds", "Copying latent thumbprints from publicly accessible land deed registries onto silicone molds for AePS fraud."),
            ("Medical Identity Theft for False Insurance Claims", "Using stolen health insurance policy numbers to file fraudulent hospitalization claims in colluding clinics.")
        ]),
        ("Government Impersonation", 14, [
            ("Fake Central Bureau of Investigation (CBI) Summons", "Sending fake letterhead notices accusing citizens of high-level corruption and demanding confidential online depositions."),
            ("Counterfeit Enforcement Directorate (ED) Money Laundering Notice", "Forging PMLA summons to extort business executives with threats of freezing company accounts."),
            ("Fake Telecom Authority (TRAI) Disconnection Call", "Automated IVR calls claiming all mobile SIMs linked to Aadhaar will be disconnected within 2 hours."),
            ("Bogus Police Cyber Cell Notice for Illegal Internet History", "Pop-up browser notices claiming local state cyber police have detected illegal browsing and require spot fine payments."),
            ("Counterfeit Supreme Court Virtual Hearing Summons", "Forging court warrants and sending fake links to virtual court hearings to intimidate citizens."),
            ("Fake National Investigation Agency (NIA) Terrorism Inquiry", "Terror-related intimidation notices threatening immediate arrest unless cleared via security bond deposits."),
            ("Bogus Municipal Corporation Demolition Notice Scam", "Extorting shopkeepers with counterfeit municipal illegal structure demolition orders."),
            ("Counterfeit GST Registration Cancellation Notice", "Targeting GST registered businesses with fake tax audit penalties requiring immediate payment."),
            ("Fake Road Transport Office (RTO) Driving License Suspension", "SMS claiming license cancellation for traffic infractions unless rectified via third-party link."),
            ("Bogus Food Safety (FSSAI) Inspection Penalty Threat", "Intimidating small restaurant owners with fake food hygiene violation notices demanding immediate settlements."),
            ("Fake Department of Posts Customs Duty Demands", "Counterfeit postal letters demanding import clearance fees for unclaimed parcels."),
            ("Bogus Intelligence Bureau Threat Alert", "Calling high-net-worth individuals claiming their family is under surveillance by foreign cartels to extract protection money."),
            ("Counterfeit High Court Contempt of Court Warrant", "Threatening government servants with fabricated judicial contempt warrants unless settled out of court."),
            ("Fake Election Commission Voter Card Revocation Notice", "Phishing SMS claiming voter registration will be purged before upcoming elections unless e-KYC is submitted.")
        ]),
        ("Digital Arrest", 12, [
            ("Skype Video Interrogation with Fake Police Station Backdrop", "Staging realistic police stations with actors in uniform on video calls to demand digital confinement."),
            ("Narcotics in Courier Packet Accusation and Virtual Confinement", "Accusing victims that 16 MDMA passports were found in a FedEx box sent from their Aadhaar."),
            ("Illegal International Bank Transfer Virtual Arrest Threat", "Falsely claiming the victim's bank account was used in a Rs 38 Crore hawala money laundering operation."),
            ("Fake CBI Officer Demanding Money in Verification Account", "Coercing victims to transfer life savings into 'Supreme Court Safe Escrow Accounts' for verification."),
            ("Counterfeit Arrest Warrant with Official Emblem Displayed on Screen", "Displaying forged warrants with national emblems and real IPS officer names during video calls."),
            ("Threat of 72-Hour Incommunicado Confinement on Video", "Forcing victims to keep webcam on 24 hours a day, forbidding contact with spouse, children, or lawyers."),
            ("False Accusation of Money Laundering via Stolen Identity", "Convincing victims that criminals registered accounts with their leaked IDs and they are prime suspects."),
            ("Fake Judge Video Hearing with Pre-recorded Courtroom Clip", "Broadcasting short pre-recorded video clips of courtroom judges to reinforce judicial authority."),
            ("Demand for Liquidating Fixed Deposits into Safe Escrow", "Forcing senior citizens to prematurely break retirement fixed deposits to deposit in fake reserve accounts."),
            ("Threat of Ruining Family Reputation via Immediate Media Broadcast", "Threatening to tip off TV news channels about impending arrest unless compliance is immediate."),
            ("Isolation Protocol Warning Victim Not to Contact Relatives", "Instructing victims that sharing the ongoing 'secret national security probe' is a non-bailable offense."),
            ("Fake Cyber Cell Digital Surveillance Tracker Deception", "Claiming the victim's phone is under real-time military satellite surveillance to prevent them from hanging up.")
        ]),
        ("Parcel and Courier Fraud", 12, [
            ("FedEx Illegal Contraband Package Seizure Call", "Interactive voice response calls claiming an outgoing international parcel contains illicit narcotics."),
            ("India Post Incomplete Delivery Address Link Phishing", "SMS claiming parcel cannot be delivered due to missing house number with a link charging a Rs 25 redelivery fee."),
            ("Customs Detention Charge Demand for Foreign Gift", "Calling recipients of supposed international gifts claiming valuable electronics are held at air cargo customs."),
            ("Damaged Courier Package Compensation Claim Phishing", "Fake email offering compensation for transit damage that prompts users for full bank card details."),
            ("Courier Rescheduling Fee Debit Card Phishing Trap", "Phishing portals designed around logistics tracking where users enter card numbers to reschedule delivery dates."),
            ("BlueDart Waybill Tracking Malware APK Download", "SMS with a link to download 'BlueDart_Express_Track.apk' which installs an SMS-stealing trojan."),
            ("Fake DHL International Express Delivery Clearance", "Fake emails claiming an express document envelope from overseas requires clearance taxes."),
            ("Air Cargo Precious Stones Clearance Duty Fraud", "Convincing victims a box of diamonds was shipped to them and requires anti-terror clearance fees."),
            ("Postal Stamp Duty Payment Phishing Link", "Fake notifications demanding payment of postal revenue stamps for legal documents."),
            ("Doorstep Courier Delivery Verification OTP Hijack", "Delivery agents asking customers for delivery OTPs before handing over parcels, then keeping the goods."),
            ("Undelivered Wedding Card Postal Trap", "Sending parcels marked 'Urgent Wedding Invitation' with Rs 300 unpaid postage to trick households into paying cash."),
            ("Fake E-Commerce Courier Tracking SMS", "Blasting millions of tracking links on festival days when almost every household expects shipments.")
        ]),
        ("Travel and Ticket Booking", 11, [
            ("Fake IRCTC Tatkal Ticket Booking Software Scam", "Selling illegal bot scripts on Telegram that steal users' IRCTC passwords and netbanking credentials."),
            ("Helicopter Booking Pass Fraud for Kedarnath & Vaishno Devi", "Cloned helicopter ticket websites taking thousands of rupees from pilgrims and issuing worthless fake boarding passes."),
            ("Ghost Airline Flight Booking on Cloned Web Portal", "Travel aggregator clone portals issuing fake PNR numbers that fail at airport check-in counters."),
            ("Fake Visa Stamping Agent for Schengen Countries", "Unregistered travel agents taking passport originals and lakhs in fees, returning fake embossed visa stickers."),
            ("Counterfeit Railway Waitlist Confirmation Guarantee", "Touts claiming guaranteed coach upgrade from waitlist for direct cash transfers."),
            ("Bogus Jungle Safari & Wildlife Sanctuary Permit Scam", "Fake national park permit portals taking booking fees for Ranthambore and Jim Corbett safaris."),
            ("Fake Cruise Holiday Voucher Package Trap", "Telemarketers claiming the victim won a free 5-star Goa cruise voucher that requires Rs 9,999 tax."),
            ("Counterfeit Bus Ticket Booking Portal during Diwali Rush", "Fake interstate bus ticket booking websites collecting non-refundable fares during holiday travel peaks."),
            ("Airport VIP Fast-Track Immigration Pass Scam", "Selling worthless electronic fast-track passes for international airport immigration."),
            ("Unregistered Travel Agent Desert Safari Advance Theft", "Collecting advance tour fees for Jaisalmer camel camps and absconding upon tourist arrival."),
            ("Fake Hotel Cancellation Refund Reversal Trap", "Intercepting hotel cancellation requests to trigger reverse UPI collect requests on victims.")
        ]),
        ("Fake Customer Support", 12, [
            ("Poisoned Google Maps Contact Number for Airline Helpdesk", "Modifying public Google Business listings for airline helpdesks with scammer mobile numbers."),
            ("Fake Twitter/X Customer Care Bot for Banking Inquiries", "Automated social bots replying to public bank complaints with WhatsApp links to phishing desks."),
            ("Counterfeit Swiggy / Zomato Food Order Refund Call", "Calling customers who complained about missing food items and triggering screen share app downloads."),
            ("Fake Gas Agency Cylinder Booking Helpline Scam", "Poisoning contact details for Indane and Bharat Gas agencies to steal online refill payments."),
            ("Counterfeit DTH Television Recharge Support Agent", "Pretending to resolve signal loss issues on Tata Play/Airtel DTH by asking for netbanking credentials."),
            ("Fake Broadband Internet Repair Executive Call", "Calling during fiber network outages to charge fake line inspection and modem upgrade fees."),
            ("Counterfeit Municipal Water Supply Grievance Number", "Fake civic helplines collecting unverified water tanker booking advances into personal accounts."),
            ("Fake Ride-Hailing App (Uber/Ola) Lost Item Support Trap", "Demanding advance security deposits via UPI to return phones lost in cabs, then keeping both."),
            ("Counterfeit Courier Parcel Locker Customer Care", "Impersonating automated parcel locker support to extract OTPs for locker theft."),
            ("Fake Insurance Claim Settlement Grievance Executive", "Calling claimants awaiting health insurance reimbursements demanding 10% processing cuts."),
            ("Counterfeit Smartphone Warranty Support Portal", "Uncertified repair portals collecting upfront inspection fees and courier charges for mobile servicing."),
            ("Fake Tollway FASTag Helpdesk Phone Scam", "Guiding callers to download remote access utilities to resolve blacklisted highway toll tags.")
        ]),
        ("Mobile and SIM-Related Scams", 12, [
            ("5G Network Upgrade SMS Code Interception", "Calling users offering free 4G-to-5G SIM upgrades while requesting OTPs to execute unauthorized SIM swaps."),
            ("Remote eSIM Activation QR Code Profile Hijack", "Convincing users to scan an eSIM profile QR code sent via email, transferring the phone line to attacker's device."),
            ("Unconditional Call Forwarding *21* Phone Deception", "Tricking victims into dialing `*21*<scammer_number>#` under guise of testing signal quality, forwarding all calls and OTPs."),
            ("Missed Call from Foreign Country International Toll Trap", "Wangiri scam: ringing once from satellite country codes (+232, +881) prompting expensive callback toll charges."),
            ("Fake Telecom Tower Installation Land Lease Scam", "Promising monthly rent of Rs 80,000 for installing Jio/Airtel towers on vacant plots in exchange for advance registration fees."),
            ("Counterfeit VIP Fancy Mobile Number Auction Trap", "Selling non-existent rare 999999 VIP phone numbers on fake telecommunication auction sites."),
            ("SIM Card Expiry Notification Threatening Service Cut", "SMS claiming the SIM card will be deactivated due to non-verification of Aadhaar KYC."),
            ("Stolen Phone IMEI Number Unblocking Payment Scam", "Extorting victims searching for lost phones with promises of police IMEI tracking reports."),
            ("Counterfeit Mobile Signal Booster Device Sales", "Selling illegal, uncertified cellular signal boosters that interfere with commercial cell towers."),
            ("Fake WhatsApp Verification Call Forwarding Trick", "Instructing victims to forward verification calls while scammers register WhatsApp on their own device."),
            ("Unauthorized Porting Request (UPC) Hijack", "Generating Unique Porting Codes without consumer consent to port numbers to other network circles."),
            ("Mobile Recharge Cashback Malware Link", "Distributing modified APK files promising free lifetime mobile recharge that harvest contacts.")
        ]),
        ("School and Student Scams", 14, [
            ("Leaked Board Exam Question Paper Telegram Racket", "Selling fabricated PDF question papers of upcoming CBSE/ICSE board exams for Rs 5,000 per subject."),
            ("Fake University Degree Certificate Verifier Scam", "Operating bogus verification portals for unaccredited private universities to pass employment screenings."),
            ("Counterfeit Government Scholarship Registration Advance", "Charging mandatory application fees for free Central government minority and merit scholarships."),
            ("Bogus Overseas University Admission Letter Trap", "Issuing counterfeit admission letters for unaccredited foreign community colleges to extract tuition advances."),
            ("Fake Medical NEET Entrance Exam Seat Allotment Scam", "Promising management quota MBBS seats in reputed medical colleges in exchange for direct cash donations."),
            ("Counterfeit Engineering College Capitation Fee Racket", "Touts claiming backdoor institutional admissions to premier IIT/NIT institutions."),
            ("Fake Internship Program with Heavy Certificate Fee", "Offering unpaid virtual internships that require students to pay Rs 2,500 for training kits and certificates."),
            ("Bogus Research Paper Publishing Journal Advance Fee", "Predatory open-access journals charging rapid publication fees for un-peer-reviewed academic articles."),
            ("Counterfeit School Teacher Recruitment Exam Paper", "Defrauding teaching aspirants with promises of leaked government primary teacher exam papers."),
            ("Fake Host Family Accommodation Booking for Foreign Studies", "Collecting foreign student accommodation deposits for properties that do not exist."),
            ("Counterfeit Student Laptop Distribution Scheme SMS", "Phishing links claiming government is distributing free laptops under digital literacy schemes."),
            ("Fake Educational Loan Subsidy Clearance Charge", "Charging upfront fees to approve interest subvention subsidies on student bank loans."),
            ("Counterfeit Campus Placement Assistance Guarantee Fee", "Placement agencies demanding non-refundable registration charges with 100% MNC interview guarantees."),
            ("Fake Student Discount Card Membership Scam", "Selling counterfeit international student identity cards that fail to provide real transit discounts.")
        ]),
        ("Family and Senior-Citizen Safety", 14, [
            ("Grandchild in Serious Traffic Accident Urgent Bail Scam", "Panicked voice calls claiming a beloved grandchild was arrested after a hit-and-run and needs immediate bail money."),
            ("Digital Life Certificate (Jeevan Pramaan) Biometric Phishing", "Scammers visiting senior citizens under guise of updating annual pension life certificates to harvest thumbprints."),
            ("Senior Citizen Fixed Deposit High Interest Trick", "Unregistered non-banking firms offering 18% interest on senior deposits, vanishing with lifetime savings."),
            ("Pension Disbursement Blocked KYC SMS Phishing", "SMS claiming monthly defense or civil pension has been stopped due to outdated bank details."),
            ("Electricity Disconnection Threatening Senior Household", "Late evening SMS warning power will be disconnected in 60 minutes unless settled via unverified link."),
            ("Fake Medical Insurance Top-Up for Ailing Seniors", "Selling worthless health insurance top-up riders to seniors with pre-existing medical conditions."),
            ("Religious Pilgrimage Tour Advance Fee Theft for Elders", "Senior pilgrimage travel packages (Char Dham, Kashi) taking advance bookings and dissolving before travel."),
            ("Ayushman Bharat Golden Card Registration Fee Fraud", "Charging fees to issue Ayushman PM-JAY health cards which are distributed free by the government."),
            ("Fake Hearing Aid and Senior Mobility Device Website", "Selling defective, dangerous hearing aids and mobility walkers on bogus health storefronts."),
            ("Senior Citizen Companionship and Caregiver Advance Scam", "Collecting placement agency deposits for trained geriatric nurses who never report for duty."),
            ("Bogus Post Office Monthly Income Scheme (MIS) Agent", "Unaccredited agents pocketing senior citizens' monthly cash deposits intended for post office accounts."),
            ("Senior Reverse Mortgage Equity Extraction Scam", "Misleading seniors into signing predatory mortgage documents transferring homeownership to private lenders."),
            ("Deceased Spouse Life Insurance Settlement Advance Fee", "Claiming unclaimed insurance policies of deceased spouses exist if administrative fees are paid."),
            ("Senior Citizen Home Healthcare Booking Trap", "Extracting advance payments for home pathology tests and medical equipment rentals without delivery.")
        ]),
        ("Deepfake and AI Impersonation", 12, [
            ("AI Cloned Voice of Son Begging for Emergency Hospital Bills", "Using 3-second audio clips from social media to synthesize a son's voice begging for immediate emergency transfer."),
            ("Deepfake Video Call of Company CEO Requesting Wire Transfer", "Joining video conferences with a live face-swapped avatar of the CEO instructing urgent vendor payments."),
            ("AI Generated Audio Snippet Threatening Kidnapping Ransom", "Sending synthesized recordings of a child crying out for help to extort ransom from frightened parents."),
            ("Deepfake Politician Video Stoking Communal Discord", "Fabricating inflammatory speeches using AI video generation during sensitive election or festival periods."),
            ("AI Cloned Celebrity Voice Promoting Bogus Trading App", "Deepfake audio of famous news anchors and film stars endorsing fraudulent cryptocurrency trading apps."),
            ("Deepfake Executive Video Approving False Procurement Contract", "Fabricating video messages of procurement directors instructing warehouse inventory releases."),
            ("AI Generated Phishing Email Replicating Boss Writing Style", "Using Large Language Models to craft flawless spear-phishing emails mimicking executive tone."),
            ("Voice Morphing Scam Impersonating Family Lawyer", "Synthesizing family legal counsel voice demanding confidential bail bonds for family members."),
            ("Deepfake Video of Bank Manager Approving Unsecured Loan", "Showing fabricated video approvals from branch managers to convince borrowers to pay processing fees."),
            ("AI Cloned Child Voice Calling School Principal for Early Release", "Calling school authorities with cloned parental voices to request early release of students."),
            ("Deepfake Video Testimonial for Fraudulent Health Cure", "Using AI to generate fake doctor testimonials endorsing unverified herbal medicines for chronic illnesses."),
            ("AI Voice Clone of Police Officer Demanding Spot Penalty", "Automated synthetic calls from senior police officials demanding electronic payments for fictitious traffic violations.")
        ]),
        ("Gaming and Online Marketplaces", 11, [
            ("OLX Indian Army Officer Furniture Moving Scam", "Pretending to be transferred military personnel selling household goods cheaply and reversing QR collect requests."),
            ("Free Fire / BGMI Free Weapon Skin Phishing Link", "Promising free diamond top-ups and rare character skins on websites designed to harvest social logins."),
            ("Counterfeit Gaming Tournament Entry Fee Theft", "Collecting registration fees for esports tournaments that are abruptly canceled without refunds."),
            ("Stolen Steam / Epic Games Account Marketplace Sale", "Selling hijacked gaming accounts with high game libraries that are recovered by original owners within days."),
            ("Roblox / Minecraft Currency Generator Phishing", "Luring young children with fake currency generators that download spyware or subscribe to premium SMS."),
            ("Fake Used Car Inspection Report Deposit on CarDekho", "Demanding upfront inspection certification charges before allowing buyers to view second-hand cars."),
            ("Counterfeit Luxury Watch Sale on Peer-to-Peer App", "Selling replica watches with counterfeit authenticity papers on classifieds platforms."),
            ("Bogus Farm Equipment Sale on Agricultural Marketplace", "Listing second-hand tractors at half price on rural marketplaces to steal booking advances."),
            ("Game Account Middleman Escrow Theft Scam", "Posing as trusted middleman on Discord/WhatsApp to steal both the game account credentials and the buyer's money."),
            ("Fake Gaming Console Hardware Modding Service Trap", "Taking expensive gaming consoles for jailbreaking/modding and absconding with customer hardware."),
            ("Counterfeit Antique Coin & Currency Buyer Scam", "Claiming rare old 1-rupee coins can be sold for Rs 5 Lakhs if the owner pays a RBI registration fee.")
        ]),
        ("Subscription and Technical Support Fraud", 11, [
            ("Microsoft Windows System Lockscreen Alert Scam", "Displaying fullscreen browser warnings with audio sirens falsely claiming the computer is infected with spyware."),
            ("Symantec Norton Antivirus Automatic Renewal Phishing Invoice", "Sending fake PDF receipts for Rs 34,999 annual subscriptions prompting victims to call cancelation hotlines."),
            ("McAfee Virus Found Loud Audio Siren Web Lock", "Triggering persistent looping audio alerts to convince seniors their banking credentials have been compromised."),
            ("Netflix Streaming Account Suspended Payment Update", "Phishing SMS claiming video streaming membership is paused due to credit card decline."),
            ("Amazon Prime Annual Subscription Double Charge Email", "Sending fake invoices claiming an accidental duplicate charge that can be refunded via AnyDesk."),
            ("Apple iCloud Storage Full Verification Phishing Trap", "Phishing emails warning photos will be permanently deleted in 24 hours unless storage is upgraded."),
            ("Counterfeit Google One Cloud Storage Expiry Notice", "Spoofed security notices harvesting Google account passwords and recovery codes."),
            ("Bogus Printer Setup and Driver Installation Scam", "Third-party websites offering printer drivers that lock computers and demand tech support fees."),
            ("Counterfeit Router Firmware Security Update Trap", "Directing home users to fake router administration portals that reconfigure DNS to malicious servers."),
            ("Fake Microsoft Office 365 License Revocation Email", "Warning corporate users their cloud office suite license has expired to steal enterprise SSO logins."),
            ("Bogus Web Hosting Account Suspension Phishing", "Targeting website owners with fake cPanel suspension notices requiring immediate credit card renewal.")
        ]),
        ("Recovery Scams", 10, [
            ("Fake Cyber Lawyer Guaranteeing 100% Stolen Crypto Recovery", "Targeting victims who already lost money in scams, promising legal recovery of assets for an advance retainer."),
            ("Counterfeit Ethical Hacker Promising UPI Fund Retrieval", "Claiming to have backdoor access to bank switches to reverse fraudulent UPI transactions for a 20% cut."),
            ("Bogus Central Bank Special Fund Recovery Cell SMS", "Impersonating an RBI asset restitution committee releasing funds to past cyber fraud victims."),
            ("Fake Cyber Cell Officer Demanding Investigation Fee", "Impersonating cyber police inspectors and demanding investigation fuel and forensic costs from victims."),
            ("Counterfeit Recovery Agency Demanding 20% Advance Retainer", "Unlicensed recovery companies exploiting desperate scam victims with bogus legal contracts."),
            ("Bogus Blockchain Asset Tracing Software Subscription", "Selling fake cryptocurrency tracing tools that display randomly generated wallet graph animations."),
            ("Fake Supreme Court Special Asset Restitution Notice", "Sending fake legal notices stating seized cartel assets are being redistributed to eligible victims."),
            ("Counterfeit Foreign Police Fund Repatriation Fee Scam", "Claiming foreign police have recovered seized offshore funds and require international wire transfer fees."),
            ("Fake Bank Ombudsman Compensation Claim Advance", "Pretending to be the RBI Ombudsman offering compensation for delayed fraud resolution if a fee is paid."),
            ("Bogus Consumer Forum Fast-Track Redressal Fee Scam", "Charging fees to file fast-track complaints on counterfeit consumer grievance portals.")
        ]),
        ("Emerging and Region-Specific Scams", 15, [
            ("FASTag Low Balance Account Suspension SMS Phishing", "Phishing SMS threatening highway toll blacklisting to steal banking credentials under guise of KYC updates."),
            ("Traffic e-Challan Pending Fine APK Download Trap", "Sending SMS with links to download malicious APK files disguised as state traffic police fine payment apps."),
            ("Wedding Invitation Card Malware APK File on WhatsApp", "Sending an APK file named 'Wedding_Invitation_Card.apk' which installs an SMS forwarder trojan."),
            ("PM Surya Ghar Muft Bijli Yojana Fake Solar Panel Portal", "Counterfeit government solar subsidy portals collecting non-refundable site inspection fees."),
            ("State Ration Card e-KYC Verification Threat SMS", "Threatening to cancel food subsidy rations unless beneficiaries submit biometric details on rogue links."),
            ("Mahila Samman Savings Certificate Counterfeit Agent", "Bogus agents collecting cash deposits for women's small savings schemes and issuing fake passbooks."),
            ("Fake Water Board Meter Reading Disconnection Notice", "SMS demanding immediate payment of disputed water bills via personal UPI to avoid line cuts."),
            ("Ladli Behna Yojana Subsidy Registration Scam", "Charging unauthorized registration fees for state welfare cash transfer schemes at fake cyber cafes."),
            ("Fake High-Court E-Challan Lok Adalat Payment Link", "Promising 90% discount on traffic fines during National Lok Adalat through counterfeit payment portals."),
            ("Bogus State Housing Board Affordable Flat Lottery Scam", "Advertising fake lottery schemes for government subsidized housing to collect application fees."),
            ("Counterfeit Toll Plaza Monthly Pass Phishing Link", "Selling discounted monthly FASTag local resident passes on unauthorized websites."),
            ("Fake Municipal Property Tax Amnesty Scheme Portal", "Collecting property tax arrears on cloned municipal portals during annual tax discount windows."),
            ("Bogus State Electric Vehicle (EV) Subsidy Application Trap", "Phishing portals claiming state green mobility subsidies for two-wheeler purchases."),
            ("Fake LPG Gas Cylinder Subsidy Re-KYC Update Phishing", "SMS claiming cooking gas subsidy is paused due to missing Aadhaar linkage."),
            ("Counterfeit Coastal Regulation Zone Land Clearance Scam", "Issuing forged environmental NOC certificates for coastal property developments.")
        ])
    ]

    for cat_name, count, items in categories_matrix:
        for title, desc in items:
            add(title, cat_name, "Critical" if "Arrest" in cat_name or "SIM" in cat_name or "Banking" in cat_name else "High",
                "Seniors" if "Senior" in cat_name or "Grandchild" in title else ("Students" if "Student" in cat_name or "Exam" in title else "All"),
                f"A citizen is targeted with an urgent notification regarding '{title}'. The situation appears realistic and pressures the victim into immediate compliance.",
                f"{desc} Scammers exploit psychological urgency, legal fear, or financial optimism to compromise security.",
                "Unsolicited messages; demand for immediate action; unofficial web links or APK files; requests for confidential OTPs or advance payments.",
                "Exploitation of fear, trust in authority, fear of missing out, or emotional attachment to family.",
                "Cease all communication immediately; do not transfer money or install applications; verify through official channels.",
                "Never share OTPs, passwords, or personal banking credentials. Do not install unknown software.",
                "Always verify government schemes on official .gov.in domains; consult official customer care numbers; maintain multi-factor authentication.",
                "Report immediately to the National Cyber Crime Reporting Portal (cybercrime.gov.in) and call 1930.",
                f"{cat_name}, Awareness, Cyber Defense, Safety Guidelines")

    return scenarios

def build_and_save_all():
    scenarios = get_complete_scenarios_list()
    json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "scam_scenarios.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(scenarios, f, indent=2, ensure_ascii=False)

    print(f"Generated {len(scenarios)} high-quality scam scenarios and saved to {json_path}")
    return scenarios

def seed_scenarios_to_db():
    scenarios = build_and_save_all()
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM scam_scenarios")
    for s in scenarios:
        cursor.execute('''
        INSERT INTO scam_scenarios (
            scenario_id, title, category, risk_level, target_audience,
            situation, how_works, warning_signs, manipulation,
            victim_actions, avoid_actions, risk_reduction, reporting_guidance,
            last_reviewed, tags, published
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
        ''', (
            s["scenario_id"], s["title"], s["category"], s["risk_level"], s["target_audience"],
            s["situation"], s["how_works"], s["warning_signs"], s["manipulation"],
            s["victim_actions"], s["avoid_actions"], s["risk_reduction"], s["reporting_guidance"],
            s["last_reviewed"], s["tags"]
        ))

    conn.commit()
    conn.close()
    print("Database successfully seeded with all scam scenarios!")

if __name__ == "__main__":
    from database import init_db
    init_db()
    seed_scenarios_to_db()

