from django.shortcuts import render
from config.decorators import login_required_with_alert
from config.image_service import generate_image


@login_required_with_alert
def image_page(request):
    prompt = ""
    image_base64 = None
    error = None

    if request.method == "POST":
        prompt = request.POST.get("prompt", "").strip()

        try:
            image_base64 = generate_image(prompt)
        except Exception as e:
            error = str(e)

    return render(request, "image/page.html", {
        "input_text": prompt,
        "image_base64": image_base64,
        "error": error,
    })
