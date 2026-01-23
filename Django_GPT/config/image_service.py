import base64
import os
import requests

HF_IMAGE_API_URL = (
    "https://api-inference.huggingface.co/models/"
    "stabilityai/stable-diffusion-xl-base-1.0"
)

HF_API_TOKEN = os.getenv("HF_API_TOKEN")


def generate_image(prompt: str) -> str:
    """
    이미지 생성 → base64 문자열 반환
    """
    if not HF_API_TOKEN:
        raise RuntimeError("HF_API_TOKEN not set")

    headers = {
        "Authorization": f"Bearer {HF_API_TOKEN}",
    }

    response = requests.post(
        HF_IMAGE_API_URL,
        headers=headers,
        json={"inputs": prompt},
        timeout=180,
    )

    if response.status_code != 200:
        raise RuntimeError(response.text)

    image_bytes = response.content
    return base64.b64encode(image_bytes).decode("utf-8")
