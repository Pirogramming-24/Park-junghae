from functools import wraps
from django.http import HttpResponse
from django.utils.html import escape

def login_required_with_alert(view_func):
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)

        next_url = escape(request.get_full_path())  # /translate/ 같은 원래 경로
        login_url = f"/accounts/login/?next={next_url}"

        # direct URL 접근 포함해서 "alert -> 이동"을 강제
        html = f"""
        <script>
          alert("로그인 후 이용해주세요");
          window.location.href = "{login_url}";
        </script>
        """
        return HttpResponse(html)
    return _wrapped
