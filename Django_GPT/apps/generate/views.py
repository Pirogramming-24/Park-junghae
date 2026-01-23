from django.shortcuts import render
from config.decorators import login_required_with_alert
from config.ai_services import run_generate
from apps.accounts.models import ChatHistory

@login_required_with_alert
def generate_page(request):
    prompt = ""
    output = ""

    if request.method == "POST":
        prompt = request.POST.get("prompt", "")
        output = run_generate(prompt)

        ChatHistory.objects.create(
            user=request.user,
            model_name="generate",
            input_text=prompt,
            output_text=output,
        )

    histories = ChatHistory.objects.filter(
        user=request.user, model_name="generate"
    ).order_by("-created_at")

    return render(request, "generate/page.html", {
        "input_text": prompt,
        "output": output,
        "histories": histories,
    })
