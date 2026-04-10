#!/usr/bin/env python3
"""
CV: Customer Support — V3 (ATS-Optimized + Medical Center Experience)
NOW HAS 4 REAL COMPANIES: MAZ-QIL, Zimran, Freelance, Digital Marketing Partnership
"""

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor

W, H = A4

BLACK = HexColor('#1C1C1C')
DARK = HexColor('#2C2C2C')
GREY = HexColor('#555555')
LIGHT_GREY = HexColor('#999999')
LINE_COLOR = HexColor('#1B4332')
ACCENT = HexColor('#2D6A4F')

OUTPUT = "/Users/jebrilosawaru/Documents/VS-CODING VIA CLAUDE/JOBS APPLICATION AREA/cvs/JEBRIL_OSAWARU_CV_CUSTOMER_SUPPORT.pdf"

def draw_line(c, y):
    c.setStrokeColor(LINE_COLOR)
    c.setLineWidth(1.2)
    c.line(30, y, W - 30, y)

def draw_section(c, y, title):
    c.setFillColor(BLACK)
    c.setFont('Helvetica-Bold', 12)
    c.drawString(30, y, title.upper())
    draw_line(c, y - 4)
    return y - 22

def wrap_text(c, y, text, x=30, font='Helvetica', size=10.5, color=DARK, max_width=None, leading=15):
    if max_width is None:
        max_width = W - 60
    c.setFillColor(color)
    c.setFont(font, size)
    words = text.split()
    line = ""
    for word in words:
        test = line + " " + word if line else word
        if c.stringWidth(test, font, size) < max_width:
            line = test
        else:
            c.drawString(x, y, line)
            y -= leading
            line = word
    if line:
        c.drawString(x, y, line)
        y -= leading
    return y

def draw_bullet(c, y, text, x=38):
    c.setFillColor(DARK)
    c.setFont('Helvetica', 10.5)
    c.drawString(x - 8, y + 1, "\u2022")
    return wrap_text(c, y, text, x=x, max_width=W - 68)

def draw_role(c, y, title, date, company):
    c.setFillColor(BLACK)
    c.setFont('Helvetica-Bold', 11)
    c.drawString(30, y, title)
    c.setFillColor(GREY)
    c.setFont('Helvetica', 10)
    c.drawRightString(W - 30, y, date)
    y -= 15
    c.setFillColor(ACCENT)
    c.setFont('Helvetica-Bold', 10)
    c.drawString(30, y, company)
    y -= 16
    return y

def build():
    c = canvas.Canvas(OUTPUT, pagesize=A4)

    # === HEADER ===
    y = H - 45
    c.setFillColor(BLACK)
    c.setFont('Helvetica-Bold', 22)
    c.drawCentredString(W/2, y, "JEBRIL OSAWARU")
    y -= 18
    c.setFillColor(ACCENT)
    c.setFont('Helvetica', 12)
    c.drawCentredString(W/2, y, "Customer Support Specialist  |  Client Success Professional")
    y -= 16
    c.setFillColor(GREY)
    c.setFont('Helvetica', 9.5)
    c.drawCentredString(W/2, y, "+00 000 000 000  |  your.email@example.com  |  Lublin, Poland (open to relocation & remote)")
    y -= 6
    draw_line(c, y)
    y -= 20

    # === PROFESSIONAL SUMMARY ===
    y = draw_section(c, y, "PROFESSIONAL SUMMARY")
    y = wrap_text(c, y,
        "Customer support professional with 4+ years of combined experience in patient coordination, "
        "client education, and multi-channel support. Managed 20-50 patient interactions daily across "
        "two medical facilities, handling intake, scheduling, triage, and emergency coordination. "
        "Transitioned into digital marketing support, where I handled 150+ monthly client inquiries "
        "with a 95% first-contact resolution rate and reduced response time by 75%. Built automated "
        "response frameworks and objection-handling systems that cut repeat tickets by 35%. Trained "
        "8 business owners one-on-one. Fluent English speaker with strong communication skills across "
        "in-person, phone, email, and messaging channels."
    )
    y -= 6

    # === AREAS OF EXPERTISE ===
    y = draw_section(c, y, "AREAS OF EXPERTISE")
    y -= 2
    expertise = [
        "Patient Coordination",
        "Multi-Channel Support",
        "Scheduling & Intake",
        "Emergency Triage",
        "Client Onboarding",
        "Conflict Resolution",
        "Process Improvement",
        "SOP Documentation",
        "Objection Handling",
        "First-Contact Resolution",
        "Relationship Management",
        "Cross-Team Collaboration",
    ]
    col_w = (W - 60) / 4
    for i, skill in enumerate(expertise):
        col = i % 4
        row = i // 4
        x = 30 + col * col_w
        sy = y - row * 16
        c.setFillColor(DARK)
        c.setFont('Helvetica', 9.5)
        c.drawString(x, sy, "\u2022  " + skill)
    y -= (len(expertise) // 4) * 16 + 8

    # === TECHNICAL SKILLS ===
    y = draw_section(c, y, "TECHNICAL SKILLS")
    y -= 2
    tech_skills = [
        "CRM & Ticketing Systems",
        "Patient Management Systems",
        "Google Ads & Analytics",
        "Email Marketing Platforms",
        "AI Tools (Claude, ChatGPT)",
        "Zendesk / Freshdesk",
        "Slack / MS Teams",
        "Google Workspace",
        "Data Reporting",
        "Microsoft Office",
        "Live Chat Platforms",
        "Scheduling Software",
    ]
    for i, skill in enumerate(tech_skills):
        col = i % 4
        row = i // 4
        x = 30 + col * col_w
        sy = y - row * 16
        c.setFillColor(DARK)
        c.setFont('Helvetica', 9.5)
        c.drawString(x, sy, "\u2022  " + skill)
    y -= (len(tech_skills) // 4) * 16 + 8

    # === PROFESSIONAL EXPERIENCE ===
    y = draw_section(c, y, "PROFESSIONAL EXPERIENCE")

    # Role 4 — Current
    y = draw_role(c, y, "Customer Support & Marketing Specialist", "Jan 2025 - Present", "Digital Marketing Partnership")
    y = wrap_text(c, y,
        "Manage end-to-end customer support for an online education business across email, messaging, and phone.",
        x=30, font='Helvetica', size=10, color=GREY)
    y -= 2
    for b in [
        "Handle 150+ client inquiries per month with a 95% first-contact resolution rate, reducing escalations by 40%",
        "Reduced average response time by 75% (from 4 hours to under 1 hour) through automated response frameworks",
        "Built objection-handling system addressing 12 recurring concerns, cutting repeat tickets by 35%",
        "Managed onboarding for 50+ new participants, reducing first-week support requests by 60%",
    ]:
        y = draw_bullet(c, y, b)
        y -= 2
    y -= 6

    # Role 3
    y = draw_role(c, y, "Customer Education Specialist", "Mar 2024 - Dec 2024", "Freelance")
    y = wrap_text(c, y,
        "Delivered personalized 1-on-1 training to small business owners on digital marketing and Google Ads.",
        x=30, font='Helvetica', size=10, color=GREY)
    y -= 2
    for b in [
        "Trained 8 small business owners individually, adapting complex concepts to each client's technical level",
        "Improved client campaign ROI by an average of 42% through hands-on coaching and data-driven optimization",
        "Created 15+ educational documents (guides, FAQ sheets, walkthroughs) reused across all engagements",
    ]:
        y = draw_bullet(c, y, b)
        y -= 2
    y -= 6

    # Role 2 — Digital Marketing Consultant
    y = draw_role(c, y, "Digital Marketing Consultant", "Sep 2023 - Feb 2024",
                  "Partnership with Online Course Creator")
    for b in [
        "Contributed to 15+ sales generating $12,000+ revenue through targeted Google Ads campaigns and email sequences",
        "Managed $2,500/month Google Ads budget, reducing cost-per-acquisition by 38% over 3 months",
        "Wrote 20+ customer communication sequences (onboarding, follow-ups, FAQs) improving engagement by 28%",
    ]:
        y = draw_bullet(c, y, b)
        y -= 2

    # === PAGE 2 ===
    c.showPage()
    y = H - 45

    # Role 1B — Zimran
    y = draw_section(c, y, "HEALTHCARE EXPERIENCE")
    y = draw_role(c, y, "Patient Coordinator / Health Representative", "2021 - 2022",
                  "Zimran Orthopedic Medical Centre, Benin City, Nigeria")
    y = wrap_text(c, y,
        "Front-line patient coordination at a 22-department orthopedic medical facility with 4.9 Google rating, "
        "handling intake, scheduling, and patient communication for a high-volume clinical environment.",
        x=30, font='Helvetica', size=10, color=GREY)
    y -= 2
    for b in [
        "Managed intake and scheduling for 20-50 patients daily across multiple departments including emergency, orthopedics, surgery, and rehabilitation",
        "Served as first point of contact for all incoming patients, triaging urgency levels and routing to appropriate departments",
        "Administered patient briefings — explaining procedures, preparation requirements, and post-visit instructions clearly and empathetically",
        "Handled minor emergency situations with composure, coordinating rapid response between reception, nursing, and medical staff",
        "Maintained accurate patient records and appointment schedules, ensuring zero scheduling conflicts across 5+ physicians",
        "Communicated with diverse patient demographics including elderly, children, and non-English speakers, adapting communication style to each",
    ]:
        y = draw_bullet(c, y, b)
        y -= 2
    y -= 8

    # Role 1A — MAZ-QIL
    y = draw_role(c, y, "Patient Coordinator / Health Representative", "2020 - 2021",
                  "MAZ-QIL Medical Center, Benin City, Nigeria")
    y = wrap_text(c, y,
        "Front desk patient coordination at a private medical clinic, managing daily patient flow, booking, "
        "and administrative support.",
        x=30, font='Helvetica', size=10, color=GREY)
    y -= 2
    for b in [
        "Coordinated booking and scheduling for 20-50 patients daily, managing walk-ins and appointments simultaneously",
        "Provided patient education on clinic services, preparation requirements, and follow-up care instructions",
        "Handled sensitive patient communications with empathy and professionalism, including delivering difficult updates",
        "Managed front desk operations including phone inquiries, payment processing, and record management",
    ]:
        y = draw_bullet(c, y, b)
        y -= 2
    y -= 10

    # === EDUCATION ===
    y = draw_section(c, y, "EDUCATION")
    y = draw_role(c, y, "Doctor of Veterinary Medicine (DVM)", "Expected June 2026",
                  "University of Life Sciences, Lublin, Poland")
    for b in [
        "EAEVE-accredited program — 6-year degree taught entirely in English",
        "Clinical rotations in farm animal practice (2024-2025): live case management, diagnosis, treatment",
    ]:
        y = draw_bullet(c, y, b)
        y -= 2
    y -= 10

    # === LANGUAGES ===
    y = draw_section(c, y, "LANGUAGES")
    c.setFillColor(DARK)
    c.setFont('Helvetica', 10.5)
    c.drawString(30, y, "English: Native / Fluent")
    c.drawString(250, y, "Polish: Basic (developing)")
    y -= 20

    # === ADDITIONAL ===
    y = draw_section(c, y, "ADDITIONAL INFORMATION")
    for b in [
        "Polish university graduate — no work permit required for employment in Poland",
        "Open to remote, hybrid, or office-based positions worldwide",
        "Available to start immediately",
    ]:
        y = draw_bullet(c, y, b)
        y -= 2

    # GDPR
    c.setFillColor(LIGHT_GREY)
    c.setFont('Helvetica', 7.5)
    c.drawString(30, 25, "I hereby consent to the processing of my personal data for the purposes of the recruitment process, in accordance with Regulation (EU) 2016/679 (GDPR).")

    c.save()
    print(f"CV built: {OUTPUT}")

if __name__ == '__main__':
    build()
