from django.shortcuts import render
from config.ai_services import run_summarize
from apps.accounts.models import ChatHistory  # 이미 쓰고 있으면 유지

def summarize_page(request):
    input_text = ""
    output = ""

    if request.method == "POST":
        input_text = request.POST.get("text", "")
        output = run_summarize(input_text)

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
            user=request.user, model_name="summarize"
        ).order_by("-created_at")

    return render(request, "summarize/page.html", {
        "input_text": input_text,
        "output": output,
        "histories": histories,
    })
