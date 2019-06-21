from django.conf.urls import url
from django.contrib.auth import views as auth_views

from core import views as core_views
from core.views import Signup, Index, Show, Delete
from django.urls import path

urlpatterns = [
    url(r'^$', core_views.home, name='home'),
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'login'}, name='logout'),
    url(r'^signup/$', Signup.as_view(), name='signup'),
    url(r'^index/$', Index.as_view()),
    path('show', Show.as_view()),
    path('delete/<int:id>/', Delete.as_view(), name='show'),
]
