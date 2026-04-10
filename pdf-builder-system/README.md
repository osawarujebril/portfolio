# PDF Builder System

Automated professional PDF generation for CVs, cover letters, reports, and business documents. Uses Python ReportLab with custom styling, precise positioning, and ATS-optimized layouts.

## Features

- Professional CV generation with custom color palettes and typography
- ATS (Applicant Tracking System) optimized layouts — clean formatting that passes automated resume scanners
- Configurable design tokens (colors, fonts, spacing) per document
- Multi-page support with headers, footers, and page numbering
- Precise pixel-level positioning using ReportLab Canvas
- Word-wrap engine for body text, bullet points, and multi-column layouts
- GDPR consent clause automation (required for Polish/EU job applications)

## Files

- `build_cv_customer_support.py` — Customer support CV builder
- `build_cv_digital_marketing.py` — Digital marketing CV builder

## Tech Stack

- Python 3
- ReportLab (PDF generation library)
- Custom text rendering and layout engine

## How It Was Built

Built using AI-assisted development with Claude Code. Each CV is tailored to specific job requirements by extracting ATS keywords from job listings and ensuring they appear naturally throughout the document. The system allows rapid generation of role-specific CVs from a single codebase.

## What This Demonstrates

- Python automation for document processing
- Professional document design and layout
- ATS optimization methodology
- Reusable template architecture
- Practical tool building for real-world job applications
