from django.urls import path
from accounts.views import user_login
from hello.views import hello
from . import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('logout/', LogoutView.as_view(next_page='hello'), name='logout'),
    path('', hello, name='hello'),
    path('login/', user_login, name='login'),
    path('Fiziognomika/', views.fiziognomika, name='fiziognomika'),
    path('interesting/', views.interesting, name='SDinteresting12'),
    path('FaceParsing/', views.face_parsing, name='faceParsing'),
    path('Celebrities/', views.celebrities, name='celebrities'),

    path('Astrology/', views.astrology, name='astrology'),
    path('ZodiacSigns/', views.zodiac_signs, name='zodiac_signs'),
    path('Synastry/', views.synastryi, name='synastry'),
    path('Solar/', views.solar, name='solar'),
    path('Natal_Chart/', views.natal_chart, name='natal_chart'),
    path('Lilith_and_Selena/', views.lilith_selena, name='lilith_selena'),
    path('Home/', views.home, name='home'),
    path('Asc_Ds/', views.asc_ds, name='asc_ds'),

    path('Graphology/', views.graphology, name='graphology'),
    path('Synastry/', views.synastryS, name='synastryS'),
    path('Story/', views.story, name='story'),
    path('Signature/', views.signature, name='signature'),
    path('Astrology/Location/', views.location, name='location'),
    path('Inter/', views.inter, name='interestingS'),
    path('Incline/', views.incline, name='incline'),

    path('numerology/', views.numerology_view, name='numerology'),
    path('sectors_and_codes/', views.my_view, name='sectors_and_codes'),
    path('meaning_of_numbers/', views.numbers_view, name='numbers'),
    path('map_calculation/', views.map_view, name='map'),
    path('destiny_number/', views.destiny_view, name='destiny')

]
