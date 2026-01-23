from django.shortcuts import render
from config.hf_client import call_hf_text_model
from apps.accounts.models import ChatHistory

MODEL_NAME = "facebook/bart-large-cnn"


def summarize_page(request):
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
            output = result[0]["summary_text"]

        if request.user.is_authenticated:
            ChatHistory.objects.create(
                user=request.user,
                model_name="summarize",
                input_text=input_text,
                output_text=output,
            )

    histories = []
    if request.user.is_authenticated:
        histories = ChatHistory.objects.filter(
            user=request.user,
            model_name="summarize"
        ).order_by("-created_at")

    return render(request, "summarize/page.html", {
        "input_text": input_text,
        "output": output,
        "histories": histories,
    })
