#!/usr/bin/env python3
"""
CV: Digital Marketing Specialist — V1 (ATS-Optimized)
Focus: Google Ads, performance marketing, email marketing, AI, copywriting, info products
4 REAL COMPANIES: MAZ-QIL, Zimran, Freelance, Digital Marketing Partnership
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

OUTPUT = "/Users/jebrilosawaru/Documents/VS-CODING VIA CLAUDE/JOBS APPLICATION AREA/cvs/JEBRIL_OSAWARU_CV_DIGITAL_MARKETING.pdf"

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
    c.drawCentredString(W/2, y, "Digital Marketing Specialist  |  Performance Marketing & Copywriting")
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
        "Digital marketing professional with 2+ years of hands-on experience in Google Ads campaign management, "
        "direct response copywriting, email marketing, and conversion optimization for information products. "
        "Managed $2,500/month ad budgets, achieving a 38% reduction in cost-per-acquisition through systematic "
        "A/B testing of 50+ ad variations. Generated $12,000+ in direct revenue from 15+ closed sales. "
        "Wrote 20+ email sequences, webinar scripts, and sales copy using 25+ proven copywriting frameworks "
        "(AIDA, PAS, Schwartz, Sugarman, Halbert). Daily AI power user — built complete marketing automation "
        "systems using Claude and ChatGPT. Trained 8 business owners on digital strategy and campaign optimization, "
        "improving their average ROI by 42%."
    )
    y -= 6

    # === AREAS OF EXPERTISE ===
    y = draw_section(c, y, "AREAS OF EXPERTISE")
    y -= 2
    expertise = [
        "Google Ads (PPC/SEM)",
        "Performance Marketing",
        "Direct Response Copy",
        "Email Marketing",
        "Conversion Optimization",
        "A/B Testing",
        "Sales Funnel Design",
        "Landing Page Copy",
        "Webinar Marketing",
        "Customer Acquisition",
        "Audience Research",
        "AI Marketing Automation",
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
        "Google Ads & Analytics",
        "Meta Ads (Facebook/IG)",
        "AI Tools (Claude, ChatGPT)",
        "Email Platforms (Mailchimp)",
        "CRM Systems (HubSpot)",
        "Landing Page Builders",
        "Conversion Tracking",
        "Prompt Engineering",
        "Google Workspace",
        "Canva / Creative Tools",
        "Data Reporting",
        "WordPress / CMS",
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
    y = draw_role(c, y, "Digital Marketing & Growth Specialist", "Jan 2025 - Present",
                  "Digital Marketing Partnership")
    y = wrap_text(c, y,
        "Lead digital marketing for an online education business — managing paid acquisition, email marketing, "
        "copywriting, webinar funnels, and AI-powered content creation.",
        x=30, font='Helvetica', size=10, color=GREY)
    y -= 2
    for b in [
        "Write all sales copy, webinar scripts, and 20+ email sequences driving prospect-to-customer conversion with 25% open rates and 8% CTR",
        "Build complete sales funnels: Google Ads > landing page > email nurture > webinar > conversion, generating $12,000+ in total revenue",
        "Developed objection-handling and follow-up frameworks that increased close rate by 15% and improved retention by 28%",
        "Integrate AI tools (Claude, ChatGPT) daily for copywriting, audience research, campaign analysis, and workflow automation",
        "Analyze campaign performance weekly, optimizing targeting, messaging, and channel allocation across 3 marketing channels",
    ]:
        y = draw_bullet(c, y, b)
        y -= 2
    y -= 6

    # Role 3
    y = draw_role(c, y, "Marketing Strategy Consultant & Educator", "Mar 2024 - Dec 2024", "Freelance")
    y = wrap_text(c, y,
        "Provided 1-on-1 strategic coaching to small business owners on Google Ads, customer acquisition, "
        "and digital marketing fundamentals.",
        x=30, font='Helvetica', size=10, color=GREY)
    y -= 2
    for b in [
        "Trained 8 business owners on Google Ads strategy, keyword research, and campaign optimization over 10+ hours per client",
        "Improved client campaign ROI by an average of 42% through data-driven optimization and audience targeting strategies",
        "Built customer avatar frameworks and lead qualification systems that reduced client cost-per-lead by 30%",
        "Created 15+ marketing educational documents (playbooks, guides, templates) reused across all client engagements",
    ]:
        y = draw_bullet(c, y, b)
        y -= 2
    y -= 6

    # Role 2
    y = draw_role(c, y, "Digital Marketing & Acquisition Consultant", "Sep 2023 - Feb 2024",
                  "Partnership with Online Course Creator")
    y = wrap_text(c, y,
        "Built and executed complete customer acquisition system through paid advertising, direct response "
        "copywriting, and email marketing for an information product business.",
        x=30, font='Helvetica', size=10, color=GREY)
    y -= 2
    for b in [
        "Generated $12,000+ in direct revenue from 15+ sales through targeted Google Ads campaigns and email funnels",
        "Managed $2,500/month Google Ads budget, reducing cost-per-acquisition by 38% through A/B testing of 50+ ad variations",
        "Wrote all sales copy, landing pages, and email follow-up sequences — 20+ automated sequences improving engagement by 28%",
        "Developed lead qualification framework that increased conversion rate from lead-to-sale by 22%",
    ]:
        y = draw_bullet(c, y, b)
        y -= 2

    # === PAGE 2 ===
    c.showPage()
    y = H - 45

    # Healthcare experience (brief — shows customer-facing background)
    y = draw_section(c, y, "EARLIER EXPERIENCE")

    y = draw_role(c, y, "Patient Coordinator / Health Representative", "2021 - 2022",
                  "Zimran Orthopedic Medical Centre, Benin City, Nigeria")
    for b in [
        "Managed front-line patient coordination for 20-50 patients daily across a 22-department medical facility",
        "Served as first point of contact — intake, scheduling, triage, patient education, and emergency coordination",
        "Developed strong communication skills handling diverse demographics including elderly, children, and non-English speakers",
    ]:
        y = draw_bullet(c, y, b)
        y -= 2
    y -= 6

    y = draw_role(c, y, "Patient Coordinator / Health Representative", "2020 - 2021",
                  "MAZ-QIL Medical Center, Benin City, Nigeria")
    for b in [
        "Coordinated booking and scheduling for 20-50 patients daily, managing walk-ins and appointments simultaneously",
        "Handled patient communications, front desk operations, phone inquiries, and record management",
    ]:
        y = draw_bullet(c, y, b)
        y -= 2
    y -= 10

    # === EDUCATION ===
    y = draw_section(c, y, "EDUCATION")
    y = draw_role(c, y, "Doctor of Veterinary Medicine (DVM)", "Expected June 2026",
                  "University of Life Sciences, Lublin, Poland")
    for b in [
        "EAEVE-accredited — 6-year degree taught entirely in English",
        "Demonstrates analytical thinking, scientific rigor, and discipline to complete a demanding degree while building a marketing career in parallel",
    ]:
        y = draw_bullet(c, y, b)
        y -= 2
    y -= 10

    # === CERTIFICATIONS ===
    y = draw_section(c, y, "CERTIFICATIONS & SPECIALIZED KNOWLEDGE")
    for b in [
        "Google Ads Campaign Management — 2+ years hands-on, $2,500/month managed, 38% CPA reduction achieved",
        "Direct Response Copywriting — 25+ frameworks mastered (AIDA, PAS, PASTOR, Schwartz, Sugarman, Halbert)",
        "AI Marketing Automation — Advanced Claude and ChatGPT for copywriting, research, campaign analysis, and content creation",
        "Email Marketing & Sequences — Launch sequences, welcome sequences, nurture campaigns, objection-handling flows",
        "Information Product Marketing — Webinar funnels, course launches, sales pages, affiliate marketing",
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
        "Open to remote positions worldwide (Europe, UK, USA, Australia, or any advanced economy)",
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
