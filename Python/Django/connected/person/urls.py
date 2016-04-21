from django.conf.urls import url
from person import views


urlpatterns = (
    url(r'^$', views.index, name='home'),
    url(r'^id(?P<profile_id>\d+)/$', views.details, name='details'),
    url(r'^register/', views.register, name='register')
)
