from llama_cloud_services import LlamaParse
from dotenv import load_dotenv
from pathlib import Path
import os


load_dotenv()
parser = LlamaParse(
    api_key=os.getenv("llamaParse"),
    verbose=True,
    premium_mode=True,
    language="en",
)


result = parser.parse("rawPdf/Canva-Userguide.pdf")


Path("markdowns").mkdir(exist_ok=True)

md_out = Path("markdowns/Canva-Userguide.md")
with md_out.open("w", encoding="utf-8") as f:
    for i, doc in enumerate(result.get_markdown_documents(split_by_page=True), start=1):
        f.write(f"## Page {i}\n\n{doc.text}\n\n---\n\n")
print(f"Markdown file created at: {md_out}")


img_dir = Path("images")
img_dir.mkdir(exist_ok=True)

image_docs = result.get_image_documents(
    include_screenshot_images=True,
    include_object_images=True,
    image_download_dir=img_dir.as_posix(),
)

for idx, img_doc in enumerate(image_docs, start=1):
    saved_path = img_doc.metadata.get("file_path")
    page_no = img_doc.metadata.get("page")
    if saved_path:
        new_name = img_dir / f"page_{page_no}_image_{idx}{Path(saved_path).suffix}"
        Path(saved_path).rename(new_name)
        print(f"Saved → {new_name}")
    else:
        print("Image metadata missing 'file_path' – skipping")
