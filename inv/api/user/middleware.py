from django.shortcuts import redirect
from django.urls import reverse

class ApprovalRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            if not request.user.is_approved and not request.user.is_superuser:
                allowed_paths = [
                    reverse('logout'),
                    reverse('approval_pending'),  # a page to show "awaiting approval"
                ]
                if request.path not in allowed_paths:
                    return redirect('awaiting_approval')
        return self.get_response(request)

