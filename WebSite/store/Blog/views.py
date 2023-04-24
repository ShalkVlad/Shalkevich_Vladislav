from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.urls import reverse_lazy
from .forms import CommentForm


def post_detail(request, post_id):
    form = CommentForm(request.POST or None, initial={'post_id': post_id})
    if request.method == 'POST' and form.is_valid():
        form.save()
        form = CommentForm(initial={'post_id': post_id})
    return render(request, 'post_detail.html', {'form': form})


class CustomLoginView(LoginView):
    template_name = 'hello/panel.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['username'] = self.request.user.username
            context['logout_url'] = reverse_lazy('logout')
        return context


def interesting(request):
    return render(request, 'Blog/Fiziognomika/Interesting.html')


def fiziognomika(request):
    return render(request, 'Blog/Fiziognomika/Fiziognomika.html')


def face_parsing(request):
    return render(request, 'Blog/Fiziognomika/FaceParsing.html')


def celebrities(request):
    return render(request, 'Blog/Fiziognomika/Celebrities.html')


def zodiac_signs(request):
    return render(request, 'Blog/Astrology/ZodiacSigns.html')


def synastryi(request):
    return render(request, 'Blog/Astrology/synastryi.html')


def solar(request):
    return render(request, 'Blog/Astrology/solar.html')


def astrology(request):
    return render(request, 'Blog/Astrology/Astrology.html')


def natal_chart(request):
    return render(request, 'Blog/Astrology/natal_chart.html')


def lilith_selena(request):
    return render(request, 'Blog/Astrology/Lilith_and_Selena.html')


def home(request):
    return render(request, 'Blog/Astrology/home.html')


def asc_ds(request):
    return render(request, 'Blog/Astrology/asc_ds.html')


def synastryS(request):
    return render(request, 'Blog/Graphology/synastry.html')


def story(request):
    return render(request, 'Blog/Graphology/story.html')


def signature(request):
    return render(request, 'Blog/Graphology/signature.html')


def location(request):
    return render(request, 'Blog/Graphology/location.html')


def inter(request):
    return render(request, 'Blog/Graphology/inter.html')


def incline(request):
    return render(request, 'Blog/Graphology/incline.html')


def graphology(request):
    return render(request, 'Blog/Graphology/graphology.html')


def my_view(request):
    return render(request, 'Blog/Numerology/Sectors_and_codes.html')


def numerology_view(request):
    return render(request, 'Blog/Numerology/Numerology.html')


def numbers_view(request):
    return render(request, 'Blog/Numerology/Destiny_Number.html')


def map_view(request):
    return render(request, 'Blog/Numerology/Map_calculation.html')


def destiny_view(request):
    return render(request, 'Blog/Numerology/Meaning_of_numbers.html')
