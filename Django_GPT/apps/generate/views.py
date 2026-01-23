from django.shortcuts import render
from config.decorators import login_required_with_alert
from config.hf_client import call_hf_text_model
from apps.accounts.models import ChatHistory

MODEL_NAME = "bigscience/bloom-560m"


@login_required_with_alert
def generate_page(request):
    prompt = ""
    output = ""

    if request.method == "POST":
        prompt = request.POST.get("prompt", "")

        result = call_hf_text_model(
            MODEL_NAME,
            {
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": 120,
                    "temperature": 0.7,
                }
            }
        )

        if isinstance(result, dict) and result.get("error"):
            output = f"모델 오류: {result['message']}"
        else:
            output = result[0]["generated_text"]

        ChatHistory.objects.create(
            user=request.user,
            model_name="generate",
            input_text=prompt,
            output_text=output,
        )

    histories = ChatHistory.objects.filter(
        user=request.user,
        model_name="generate"
    ).order_by("-created_at")

    return render(request, "generate/page.html", {
        "input_text": prompt,
        "output": output,
        "histories": histories,
    })
