from pathlib import Path
import base64
from datetime import datetime
import os
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

openai_key = os.getenv("OPENAI_API_KEY")
openai_client = OpenAI(api_key=openai_key)


DATA_DIR = Path(__file__).resolve().parent
IMAGES_DIR = DATA_DIR / "images"
MARKDOWN_DIR = DATA_DIR / "markdowns"
MARKDOWN_DIR.mkdir(parents=True, exist_ok=True)


def markdown_from_image(image_path: Path) -> str:
    """Return Markdown description of a instructional poster / screenshot."""
    system_prompt = """ 
        You are an expert technical writer specialized in generating step-by-step platform usage instructions from visual guides and screenshots.

        You will receive an image that shows a Canva platform interface along with embedded instructions (text + UI reference). Your job is to carefully convert this image into a highly detailed, structured Markdown guide that explains how a user can perform the task shown.

        Requirements:
        - Break down the process into step-by-step clickable instructions, as if teaching a new user.

        - Be explicit about what to click, where to find it, and what happens next.

        - Use Markdown with clear headings (#, ##) and numbered lists for instructions.

        - If any buttons, menus, or input boxes are shown, describe:

            - Button text or icon

            - Exact screen location (e.g., "top-left", "sidebar", "below the search bar")

            - Expected result after clicking

        - Keep all visual cues and labels in your instruction to help map back to the interface.

        - Do not summarize—output should be complete, granular instructions.

        Do not include commentary or assumptions. Only return Markdown instructions that reflect exactly what is visible in the image.
        """

    img_bytes = image_path.read_bytes()
    b64 = base64.b64encode(img_bytes).decode()
    data_url = f"data:image/{image_path.suffix.lstrip('.').lower()};base64,{b64}"

    rsp = openai_client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Please convert this Canva how-to poster into Markdown.",
                    },
                    {"type": "image_url", "image_url": {"url": data_url}},
                ],
            },
        ],
        temperature=0,
    )
    return rsp.choices[0].message.content.strip()


def convert_all_images():
    supported = {".png", ".jpg", ".jpeg", ".webp"}

    for image_path in IMAGES_DIR.iterdir():
        if image_path.suffix.lower() not in supported:
            continue

        print(f"🔍  Converting {image_path.name} …")
        md = markdown_from_image(image_path)

        ts = datetime.now().strftime("%Y%m%d")
        stem = image_path.stem.replace(" ", "_")
        out = MARKDOWN_DIR / f"{stem}_{ts}.md"
        out.write_text(md, encoding="utf-8")
        print(f"✅  Saved ")


if __name__ == "__main__":
    convert_all_images()
