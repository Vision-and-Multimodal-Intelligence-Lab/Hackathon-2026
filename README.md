# Hackathon 2026 Poster Generation Reference

This repository is a reference implementation for a **Hackathon 2026 poster generation project**.

It demonstrates how to use Python with the OpenRouter API and the model:

- `google/gemini-3.1-flash-image-preview`

If you want examples in other SDKs/languages, see the official OpenRouter API page:

- https://openrouter.ai/google/gemini-3.1-flash-image-preview/api

## What This Reference Code Covers

- Calling OpenRouter from Python via the OpenAI-compatible client
- Building multimodal user input:
  - pure text
  - pure image
  - text + multiple images
- Sending local image files (auto-encoded to Base64 data URLs)
- Decoding generated Base64 image outputs and saving to disk

## Project Structure

- `example.py`: main reference script
- `resource/`: input image assets for prompts
- `generated_images/`: output folder for generated poster images

## Requirements

- Python 3.10+
- `openai` Python package

Install dependency:

```bash
pip install openai
```

## Quick Start

1. Open `example.py`
2. Set your OpenRouter API key:

```python
API_KEY = "ENTER_YOUR_KEY_HERE"
```

3. Configure input mode and prompt:

```python
INPUT_MODE = "text+image"  # "pure text" | "pure image" | "text+image"
INPUT_TEXT = "Your poster instructions..."
INPUT_IMAGES = ["resource/flyer.jpeg", "resource/speaker image.jpg"]
```

4. Run:

```bash
python example.py
```

Generated images will be saved in `generated_images/`.

## Input Modes

### 1) Pure Text

Use only a text prompt:

```python
INPUT_MODE = "pure text"
INPUT_TEXT = "Design a clean academic seminar poster..."
INPUT_IMAGES = []
```

### 2) Pure Image

Use one or more reference images without text:

```python
INPUT_MODE = "pure image"
INPUT_IMAGES = ["resource/flyer.jpeg"]
```

### 3) Text + Image (Recommended for poster tasks)

Combine instructions with one or more references:

```python
INPUT_MODE = "text+image"
INPUT_TEXT = "Create a CS seminar poster in this style..."
INPUT_IMAGES = ["resource/flyer.jpeg", "resource/speaker image.jpg"]
```

## Notes

- This repo is meant as **reference code** for hackathon development, not a production-ready framework.
- Keep your API key private. Do not commit real keys to public repositories.
- Model behavior and output format may change over time; always verify against the latest OpenRouter docs.

## Official Documentation

- OpenRouter model API page: https://openrouter.ai/google/gemini-3.1-flash-image-preview/api
