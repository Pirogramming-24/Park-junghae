from django.shortcuts import render
from config.decorators import login_required_with_alert
from config.hf_client import call_hf_image_model
import base64

MODEL_NAME = "stabilityai/stable-diffusion-xl-base-1.0"


@login_required_with_alert
def image_page(request):
    prompt = ""
    image_base64 = None
    error = None

    if request.method == "POST":
        prompt = request.POST.get("prompt", "")

        result = call_hf_image_model(
            MODEL_NAME,
            {"inputs": prompt}
        )

        if isinstance(result, dict) and result.get("error"):
            error = result["message"]
        else:
            image_base64 = base64.b64encode(result).decode("utf-8")

    return render(request, "image/page.html", {
        "input_text": prompt,
        "image_base64": image_base64,
        "error": error,
    })
