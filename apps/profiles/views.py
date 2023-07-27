from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from .models import UserProfile


class Profile(TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        profile = get_object_or_404(UserProfile, user=self.request.user)
        context['profile'] = profile
        return context
