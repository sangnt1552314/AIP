from django.conf.urls import url
from AIP import views

app_name = 'AIP'

urlpatterns =[
    url(r'^$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^show/', views.show, name='show'),
    url(r'^canny/', views.canny, name='canny'),
    url(r'^hough/', views.hough, name='hough'),
    url(r'^faq/', views.faq, name='faq'),
    url(r'^extract/', views.extract, name='extract'),
    url(r'^reset/', views.reset, name='reset'),
]
