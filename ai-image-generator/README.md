# AI Image Generator

Python scripts that interface with the Kie.ai API to generate hyper-realistic AI images from structured JSON prompts. Supports image generation, image editing, and image-to-video conversion.

## Features

- Generate AI images from structured JSON prompt files
- Edit existing images with AI-powered modifications
- Convert AI-generated images to short video clips
- Configurable aspect ratios and output settings
- Environment variable management for API key security

## Files

- `generate_kie.py` — Core image generation script
- `edit_kie.py` — Image editing and modification script
- `generate_kie_video.py` — Image-to-video conversion script

## Tech Stack

- Python 3
- Kie.ai API (Nano Banana 2 model)
- Requests library for HTTP communication
- JSON for structured prompt management
- Environment variables for secure API key handling

## Usage

```bash
python generate_kie.py prompt.json output.png 16:9
```

Where `prompt.json` contains a structured prompt designed to produce hyper-realistic output with controlled composition, lighting, and subject positioning.

## How It Was Built

Built using AI-assisted development with Claude Code. The structured JSON prompting approach was developed to overcome the common "AI plastic look" problem in generated images, producing output that closely resembles professional photography.

## What This Demonstrates

- API integration and HTTP request handling
- Structured data processing (JSON)
- Environment variable security practices
- AI tool integration for creative production
- Command-line tool development
