from django.shortcuts import render
from config.decorators import login_required_with_alert
from config.ai_services import run_sentiment
from apps.accounts.models import ChatHistory

@login_required_with_alert
def sentiment_page(request):
    input_text = ""
    output = ""

    if request.method == "POST":
        input_text = request.POST.get("text", "")
        output = run_sentiment(input_text)

        ChatHistory.objects.create(
            user=request.user,
            model_name="sentiment",
            input_text=input_text,
            output_text=output,
        )

    histories = ChatHistory.objects.filter(
        user=request.user, model_name="sentiment"
    ).order_by("-created_at")

    return render(request, "sentiment/page.html", {
        "input_text": input_text,
        "output": output,
        "histories": histories,
    })
