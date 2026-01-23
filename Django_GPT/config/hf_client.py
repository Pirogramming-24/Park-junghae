import requests
from django.conf import settings

TEXT_API_BASE = "https://api-inference.huggingface.co/models"
ROUTER_API_BASE = "https://router.huggingface.co/hf-inference/models"


def call_hf_text_model(model_name, payload, timeout=120):
    """
    텍스트 모델 전용 (요약, 생성, 번역)
    """
    url = f"{TEXT_API_BASE}/{model_name}"

    response = requests.post(
        url,
        headers={
            "Authorization": f"Bearer {settings.HF_API_TOKEN}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=timeout,
    )

    if response.status_code != 200:
        return {
            "error": True,
            "message": response.text,
        }

    try:
        return response.json()
    except Exception:
        return {
            "error": True,
            "message": "JSON decode error",
        }


def call_hf_router_text_model(model_name, payload, timeout=120):
    """
    Router 기반 텍스트 모델 (감정분석)
    """
    url = f"{ROUTER_API_BASE}/{model_name}"

    response = requests.post(
        url,
        headers={
            "Authorization": f"Bearer {settings.HF_API_TOKEN}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=timeout,
    )

    if response.status_code != 200:
        return {
            "error": True,
            "message": response.text,
        }

    return response.json()


def call_hf_image_model(model_name, payload, timeout=180):
    """
    이미지 생성 (SDXL)
    """
    url = f"{ROUTER_API_BASE}/{model_name}"

    response = requests.post(
        url,
        headers={
            "Authorization": f"Bearer {settings.HF_API_TOKEN}",
        },
        json=payload,
        timeout=timeout,
    )

    if response.status_code != 200:
        return {
            "error": True,
            "message": response.text,
        }

    return response.content
