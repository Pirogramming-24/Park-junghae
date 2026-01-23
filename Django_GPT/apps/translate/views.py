from django.shortcuts import render
from config.decorators import login_required_with_alert
from config.hf_client import call_hf_text_model
from apps.accounts.models import ChatHistory

MODEL_NAME = "Helsinki-NLP/opus-mt-en-ko"


@login_required_with_alert
def translate_page(request):
    input_text = ""
    output = ""

    if request.method == "POST":
        input_text = request.POST.get("text", "")

        result = call_hf_text_model(
            MODEL_NAME,
            {"inputs": input_text}
        )

        if isinstance(result, dict) and result.get("error"):
            output = f"모델 오류: {result['message']}"
        else:
            output = result[0]["translation_text"]

        ChatHistory.objects.create(
            user=request.user,
            model_name="translate",
            input_text=input_text,
            output_text=output,
        )

    histories = ChatHistory.objects.filter(
        user=request.user,
        model_name="translate"
    ).order_by("-created_at")

    return render(request, "translate/page.html", {
        "input_text": input_text,
        "output": output,
        "histories": histories,
    })
