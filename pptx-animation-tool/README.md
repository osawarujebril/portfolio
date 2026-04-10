# PPTX Animation Tool

A Python tool that adds click-to-reveal animations to PowerPoint presentations. Solves a known limitation in python-pptx, which does not support slide animations natively.

## The Problem

python-pptx is the standard Python library for creating PowerPoint files programmatically. However, it has no support for animations — meaning any slides generated with python-pptx are static. For webinar presentations and sales decks where progressive reveal (click-to-advance) is essential, this is a significant limitation.

## The Solution

This tool injects the correct OOXML animation XML directly into slide elements after they are created by python-pptx. It adds support for:

- `appear_on_click` — Element instantly appears when the presenter clicks
- `fade_on_click` — Element fades in smoothly when the presenter clicks
- Sequenced animations — Multiple elements animated in order on a single slide
- Progressive reveal decks — Entire presentations built with click-to-advance pacing

## Files

- `pptx_animations.py` — Core animation injection library
- `pptx_progressive.py` — Progressive reveal deck builder that uses the animation library

## Tech Stack

- Python 3
- python-pptx
- lxml (for OOXML manipulation)

## Usage

```python
from pptx_animations import add_appear_on_click, add_fade_on_click

slide = prs.slides.add_slide(layout)
title = slide.shapes.add_textbox(...)
subtitle = slide.shapes.add_textbox(...)

add_appear_on_click(slide, title, order=1)
add_fade_on_click(slide, subtitle, order=2)
```

## How It Was Built

Built using AI-assisted development with Claude Code. The OOXML animation schema was reverse-engineered by examining PowerPoint files that contained animations, then the correct XML structure was replicated programmatically.

## What This Demonstrates

- Python development and library extension
- Problem-solving for a real technical limitation
- XML/OOXML manipulation
- Understanding of file format internals
- Tool building for practical production use
