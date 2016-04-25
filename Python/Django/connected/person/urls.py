from django.conf.urls import url
from person import views


urlpatterns = (
    url(r'^$', views.index, name='home'),
    url(r'^id(?P<profile_id>\d+)/$', views.details, name='details'),
    url(r'^register/', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^id(?P<profile_id>\d+)/edit/$', views.edit, name='edit'),
)
