from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy



class CustomLoginView(LoginView):
    template_name = 'hello/panel.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['username'] = self.request.user.username
            context['logout_url'] = reverse_lazy('logout')
        return context


def hello(request):
    return render(request, 'hello/TITLE.html')


def parsing_order(request):
    return render(request, 'hello/Parsing_order.html')


def feedback(request):
    return render(request, 'hello/Feedback.html')
