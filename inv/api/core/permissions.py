from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
from django.shortcuts import redirect

class AdminRequiredMixin(UserPassesTestMixin):
    # Default redirect URL if not set
    redirect_url = '/'

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def handle_no_permission(self):
        messages.warning(self.request, "You are not authorized to perform this action.")
        # Use class attribute
        return redirect(getattr(self, 'redirect_url', '/'))
        # Alternatively, you can use a named URL pattern
        # return redirect('dashboard:dashboard')  # Example named URL pattern
