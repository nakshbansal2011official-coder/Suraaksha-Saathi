import os
from PIL import Image, ImageDraw, ImageFont

IMAGES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static", "images")
os.makedirs(IMAGES_DIR, exist_ok=True)

POSTERS_CONFIG = [
    {
        "filename": "poster_1930_helpline.png",
        "title": "NATIONAL CYBER HELPLINE 1930",
        "subtitle": "ACT IN THE GOLDEN HOUR",
        "theme": "indigo",
        "accent": (244, 63, 94),     # Coral
        "bg_top": (10, 14, 39),      # Midnight Indigo
        "bg_bot": (19, 29, 64),
        "key_points": [
            "Dial 1930 immediately if you face unauthorized online banking or UPI debit",
            "Report within the first 2 hours ('Golden Hour') to freeze funds in transit",
            "Keep transaction ID, UTR number, and sender account details handy",
            "Also register on the official portal: https://cybercrime.gov.in"
        ],
        "badge": "OFFICIAL NATIONAL PROTOCOL",
        "footer": "Surakshaa Saathi Public Safety Mission | Verified Guidelines"
    },
    {
        "filename": "poster_qr_truth.png",
        "title": "THE TRUTH ABOUT QR CODES",
        "subtitle": "QR IS ONLY FOR PAYING — NEVER RECEIVING",
        "theme": "teal",
        "accent": (6, 182, 212),     # Luminous Teal
        "bg_top": (6, 24, 34),
        "bg_bot": (10, 48, 64),
        "key_points": [
            "Never scan a QR code to receive money into your bank or UPI account",
            "Scanning a QR code ALWAYS initiates an outward payment (DEBIT)",
            "No UPI PIN or password is ever required to receive money",
            "Decline any 'Collect Request' or QR scan sent by online buyers"
        ],
        "badge": "NPCI UPI SAFETY DIRECTIVE",
        "footer": "Stay Aware. Stay Secure. Stay Ahead. | Surakshaa Saathi"
    },
    {
        "filename": "poster_digital_arrest.png",
        "title": "DIGITAL ARREST IS 100% FAKE",
        "subtitle": "POLICE NEVER ARREST OVER SKYPE OR VIDEO CALL",
        "theme": "violet",
        "accent": (168, 85, 247),    # Electric Violet
        "bg_top": (22, 12, 45),
        "bg_bot": (46, 16, 85),
        "key_points": [
            "There is NO legal provision for 'Digital Arrest' under Indian law",
            "Police, CBI, ED, and Customs NEVER conduct arrests on video calls",
            "Never transfer money to any 'Supreme Court Safe Escrow Account'",
            "Disconnect video calls immediately and dial 1930 without fear"
        ],
        "badge": "PUBLIC CYBERCRIME ALERT",
        "footer": "Protect Your Family & Rights | Surakshaa Saathi Guidance"
    },
    {
        "filename": "poster_banking_rules.png",
        "title": "5 GOLDEN RULES OF SAFE BANKING",
        "subtitle": "STRENGTHEN YOUR DIGITAL ARMOR",
        "theme": "emerald",
        "accent": (16, 185, 129),    # Emerald Green
        "bg_top": (5, 30, 22),
        "bg_bot": (12, 58, 44),
        "key_points": [
            "Rule 1: Never share OTP, CVV, Netbanking password or UPI PIN with anyone",
            "Rule 2: Lock your Aadhaar Biometrics using the official mAadhaar application",
            "Rule 3: Disable international transactions and set daily card usage limits",
            "Rule 4: Never install remote-access apps (AnyDesk, TeamViewer) at caller's request",
            "Rule 5: Verify links: Official government portals strictly end in .gov.in or .nic.in"
        ],
        "badge": "RBI & CYBER DOST DIRECTIVE",
        "footer": "Empowering Citizens with Digital Hygiene | Surakshaa Saathi"
    },
    {
        "filename": "poster_senior_safety.png",
        "title": "SENIOR CITIZEN CYBER DEFENSE",
        "subtitle": "PROTECTING ELDERS FROM CALL & UTILITY FRAUDS",
        "theme": "amber",
        "accent": (245, 158, 11),    # Warm Amber
        "bg_top": (35, 25, 8),
        "bg_bot": (65, 42, 12),
        "key_points": [
            "Beware of evening SMS threatening immediate electricity or water disconnection",
            "Utility boards never send 1-hour power cut notices from 10-digit mobile numbers",
            "Beware of calls claiming a grandchild had an accident and urgently needs bail money",
            "Never allow strangers to update pension life certificates without family presence"
        ],
        "badge": "FAMILY & SENIOR CARE PROTOCOL",
        "footer": "Dedicated to Elder Protection | Surakshaa Saathi National Mission"
    },
    {
        "filename": "poster_student_safety.png",
        "title": "STUDENT & YOUTH CYBER DEFENSE",
        "subtitle": "OUTSMARTING TASK SCAMS & FAKE PAPERS",
        "theme": "blue",
        "accent": (59, 130, 246),    # Blue
        "bg_top": (10, 20, 50),
        "bg_bot": (20, 45, 95),
        "key_points": [
            "Telegram groups promising Rs 5,000/day for liking videos are fraudulent task scams",
            "Never pay money to receive a job, internship, or work-from-home assignment",
            "Beware of leaked exam question paper rackets; they sell fake PDFs and extort students",
            "Never borrow from unverified instant loan apps that demand access to your contacts"
        ],
        "badge": "YOUTH EMPOWERMENT MISSION",
        "footer": "Safe Learning for Future Leaders | Surakshaa Saathi"
    }
]

def draw_poster(config):
    width, height = 1200, 1600
    img = Image.new("RGBA", (width, height), config["bg_top"])
    draw = ImageDraw.Draw(img)

    # Vertical gradient
    r1, g1, b1 = config["bg_top"]
    r2, g2, b2 = config["bg_bot"]
    for y in range(height):
        factor = y / height
        r = int(r1 + (r2 - r1) * factor)
        g = int(g1 + (g2 - g1) * factor)
        b = int(b1 + (b2 - b1) * factor)
        draw.line([(0, y), (width, y)], fill=(r, g, b, 255))

    # Border with rounded styling
    accent = config["accent"]
    draw.rectangle([40, 40, width - 40, height - 40], outline=accent, width=4)
    draw.rectangle([52, 52, width - 52, height - 52], outline=(255, 255, 255, 60), width=2)

    # Try to load default font
    try:
        font_title = ImageFont.truetype("arialbd.ttf", 46)
        font_sub = ImageFont.truetype("arial.ttf", 30)
        font_badge = ImageFont.truetype("arialbd.ttf", 24)
        font_body = ImageFont.truetype("arial.ttf", 28)
        font_footer = ImageFont.truetype("arial.ttf", 22)
    except:
        font_title = font_sub = font_badge = font_body = font_footer = ImageFont.load_default()

    # Brand Header
    draw.text((width // 2, 90), "SURAKSHAA SAATHI", fill=(255, 255, 255, 230), font=font_sub, anchor="mm")
    draw.text((width // 2, 130), "NATIONAL CYBER SAFETY INITIATIVE", fill=accent, font=font_badge, anchor="mm")
    draw.line([(width // 2 - 200, 155), (width // 2 + 200, 155)], fill=accent, width=2)

    # Top Badge
    badge_text = config["badge"]
    draw.rectangle([(width // 2 - 220, 190), (width // 2 + 220, 240)], fill=(0, 0, 0, 140), outline=accent, width=2)
    draw.text((width // 2, 215), badge_text, fill=accent, font=font_badge, anchor="mm")

    # Main Title
    draw.text((width // 2, 330), config["title"], fill=(255, 255, 255), font=font_title, anchor="mm")
    draw.text((width // 2, 400), config["subtitle"], fill=accent, font=font_sub, anchor="mm")

    # Shield / Graphic Area Box
    draw.rounded_rectangle([120, 460, width - 120, 700], radius=20, fill=(255, 255, 255, 15), outline=(255, 255, 255, 40), width=2)
    draw.text((width // 2, 540), "PROTECT YOUR DIGITAL IDENTITY", fill=(255, 255, 255), font=font_sub, anchor="mm")
    draw.text((width // 2, 600), "VERIFIED EMERGENCY DEFENSE GUIDELINES", fill=accent, font=font_badge, anchor="mm")
    draw.text((width // 2, 650), "STAY AWARE • STAY SECURE • STAY AHEAD", fill=(200, 210, 230), font=font_footer, anchor="mm")

    # Key Points Section
    y_pos = 760
    for idx, point in enumerate(config["key_points"]):
        # Pill indicator
        draw.ellipse([140, y_pos - 8, 180, y_pos + 32], fill=accent)
        draw.text((160, y_pos + 12), str(idx + 1), fill=(10, 14, 39), font=font_badge, anchor="mm")
        
        # Text wrapping simulation
        words = point.split()
        lines = []
        cur_line = ""
        for w in words:
            if len(cur_line + " " + w) > 55:
                lines.append(cur_line)
                cur_line = w
            else:
                cur_line = cur_line + " " + w if cur_line else w
        if cur_line:
            lines.append(cur_line)

        for l_idx, line in enumerate(lines):
            draw.text((210, y_pos + (l_idx * 38)), line, fill=(245, 245, 250), font=font_body)
        
        y_pos += max(85, len(lines) * 40 + 25)

    # Helpline Callout Box
    draw.rounded_rectangle([120, 1370, width - 120, 1470], radius=15, fill=(244, 63, 94, 40), outline=(244, 63, 94), width=2)
    draw.text((width // 2, 1405), "IMMEDIATE CYBERCRIME REPORTING HELPLINE: 1930", fill=(255, 255, 255), font=font_badge, anchor="mm")
    draw.text((width // 2, 1445), "OFFICIAL PORTAL: https://cybercrime.gov.in", fill=(255, 220, 225), font=font_footer, anchor="mm")

    # Footer
    draw.text((width // 2, 1520), config["footer"], fill=(180, 190, 210), font=font_footer, anchor="mm")

    output_path = os.path.join(IMAGES_DIR, config["filename"])
    img.save(output_path, "PNG")
    print(f"Generated poster: {output_path}")

def generate_all():
    for p in POSTERS_CONFIG:
        draw_poster(p)
    print("All 6 high-resolution cyber safety posters created successfully!")

if __name__ == "__main__":
    generate_all()

