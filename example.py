import base64
import re
from datetime import datetime
from pathlib import Path
from typing import Any, cast

from openai import OpenAI

API_KEY = "ENTER_YOUR_KEY_HERE"


def save_base64_image(data_url: str, output_dir: str = "generated_images") -> Path:
    """Decode a Base64 image data URL and save it to disk."""
    match = re.match(r"^data:(image/[a-zA-Z0-9.+-]+);base64,(.+)$", data_url)
    if not match:
        raise ValueError("Invalid image data URL format")

    mime_type, b64_data = match.groups()
    ext_map = {
        "image/png": "png",
        "image/jpeg": "jpg",
        "image/webp": "webp",
        "image/gif": "gif",
    }
    file_ext = ext_map.get(mime_type, "png")

    image_bytes = base64.b64decode(b64_data)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    filename = f"generated_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.{file_ext}"
    file_path = output_path / filename
    file_path.write_bytes(image_bytes)
    return file_path


def to_image_data_url(image_input: str) -> str:
    """Return an image URL/data URL accepted by OpenRouter.

    If `image_input` is a local file path, encode it as a Base64 data URL.
    If it already looks like an http(s) URL or data URL, return as-is.
    """
    if image_input.startswith(("http://", "https://", "data:image/")):
        return image_input

    image_path = Path(image_input)
    if not image_path.exists() or not image_path.is_file():
        raise FileNotFoundError(f"Image not found: {image_input}")

    suffix = image_path.suffix.lower()
    mime_map = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp",
        ".gif": "image/gif",
    }
    mime_type = mime_map.get(suffix, "image/png")
    encoded = base64.b64encode(image_path.read_bytes()).decode("utf-8")
    return f"data:{mime_type};base64,{encoded}"


def build_user_message(mode: str, text: str | None = None, image_inputs: list[str] | None = None) -> dict[str, Any]:
    """Build a user message for pure text / pure image / text+image.

    `image_inputs` accepts multiple local paths, URLs, or data URLs.
    """
    normalized_mode = mode.strip().lower()

    if normalized_mode == "pure text":
        if not text:
            raise ValueError("'pure text' mode requires text")
        return {"role": "user", "content": text}

    if normalized_mode == "pure image":
        if not image_inputs:
            raise ValueError("'pure image' mode requires at least one image in image_inputs")
        return {
            "role": "user",
            "content": [
                {"type": "image_url", "image_url": {"url": to_image_data_url(image_input)}}
                for image_input in image_inputs
            ],
        }

    if normalized_mode == "text+image":
        if not text or not image_inputs:
            raise ValueError("'text+image' mode requires text and at least one image in image_inputs")
        image_parts = [
            {"type": "image_url", "image_url": {"url": to_image_data_url(image_input)}} for image_input in image_inputs
        ]
        return {
            "role": "user",
            "content": [
                {"type": "text", "text": text},
                *image_parts,
            ],
        }

    raise ValueError("mode must be one of: 'pure text', 'pure image', 'text+image'")


client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_KEY,
)

# Input mode: choose one of "pure text", "pure image", "text+image"
INPUT_MODE = "text+image"
INPUT_TEXT = """
Create a poster for computer science department seminar at the University of Mississippi, the following is the information:

Date: March 17, 2027
Time: 5:00 PM

Title: Generative AI for psychology 

Speaker: Dr. Adam Lee

Abstract: 
Technological intervention to support care areas that some people may not have access to is of paramount importance to promote sustainable development of good health and wellbeing. This study aims
to explore the linguistic similarities and differences between human professionals and Generative Artificial Intelligence (AI) conversational agents in therapeutic dialogues. 

Short bio of the speaker:
Dr. Adam Lee obtained his PhD in computer science from MIT. He's research scientist at Google DeepMind. 

I also provide an example invited talk poster here, please use it and follow its style and layout. I also upload the headshot of the speaker here.
"""
# You can pass local file paths, image URLs, or data URLs here
INPUT_IMAGES = ["resource/flyer.jpeg", "resource/speaker image.jpg"]

user_message = build_user_message(
    mode=INPUT_MODE,
    text=INPUT_TEXT,
    image_inputs=INPUT_IMAGES,
)
user_message = cast(Any, user_message)

# Generate an image
response = client.chat.completions.create(
    model="google/gemini-3.1-flash-image-preview",
    messages=[user_message],
    extra_body={"modalities": ["image", "text"]},
)

# The generated image will be in the assistant message
response = response.choices[0].message
images = getattr(response, "images", None)
if images:
    for image in images:
        image_url = image["image_url"]["url"]
        saved_path = save_base64_image(image_url)
        print(f"Saved image to: {saved_path}")
else:
    print("No images were returned in the response.")
