from django.shortcuts import render
from config.decorators import login_required_with_alert
from config.hf_client import call_hf_router_text_model
from apps.accounts.models import ChatHistory

MODEL_NAME = "cardiffnlp/twitter-roberta-base-sentiment-latest"


@login_required_with_alert
def sentiment_page(request):
    input_text = ""
    output = ""

    if request.method == "POST":
        input_text = request.POST.get("text", "")

        result = call_hf_router_text_model(
            MODEL_NAME,
            {"inputs": input_text}
        )

        if isinstance(result, dict) and result.get("error"):
            output = f"모델 오류: {result['message']}"
        else:
            predictions = result[0]
            best = max(predictions, key=lambda x: x["score"])

            label_map = {
                "negative": "부정",
                "neutral": "중립",
                "positive": "긍정",
            }

            output = f"{label_map[best['label']]} ({best['score']:.2f})"

        ChatHistory.objects.create(
            user=request.user,
            model_name="sentiment",
            input_text=input_text,
            output_text=output,
        )

    histories = ChatHistory.objects.filter(
        user=request.user,
        model_name="sentiment"
    ).order_by("-created_at")

    return render(request, "sentiment/page.html", {
        "input_text": input_text,
        "output": output,
        "histories": histories,
    })
