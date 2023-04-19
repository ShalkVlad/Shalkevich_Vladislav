from django.contrib.auth.views import LoginView
from django.shortcuts import render, get_object_or_404, redirect
from .models import News, Comments
from .forms import CommentForm
from datetime import datetime, timedelta


def news_list(request):
    """Вывод всех новостей
    """
    news = News.objects.all()
    return render(request, "news/news_list.html", {"news": news})


def new_single(request, pk):
    """Вывод полной статьи
    """
    new = get_object_or_404(News, id=pk)
    comment = Comments.objects.filter(new=pk, moderation=True)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.new = new
            form.save()
            return redirect(new_single, pk)
    else:
        form = CommentForm()
    return render(request, "news/new_single.html",
                  {"new": new,
                   "comments": comment,
                   "form": form})


def news_filter(request, pk):
    """ Фильтр статей по дате
    """
    news = News.objects.all()
    if pk == 1:
        now = datetime.now() - timedelta(minutes=60 * 24 * 7)
        news = news.filter(created__gte=now)
    elif pk == 2:
        now = datetime.now() - timedelta(minutes=60 * 24 * 30)
        news = news.filter(created__gte=now)
    elif pk == 3:
        news = news

    return render(request, "news/news_list.html", {"news": news})


class CustomLoginView(LoginView):
    template_name = 'Blog/panel.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['username'] = self.request.user.username
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
