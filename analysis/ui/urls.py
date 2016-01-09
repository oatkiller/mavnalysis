from django.conf.urls import include, url
from ui.views.index import index, post_details, LoginView
from ui.views import WorkoutDetailView, AddSetView
from django.contrib import admin
from django.contrib.auth import views as auth_views

urlpatterns = [
		url(r'^login', auth_views.login, { 'template_name': 'login.html' }, name='login'),
		url(r'^logout', auth_views.logout, name='logout', kwargs={'next_page': '/'}),
    url(r'^admin', include(admin.site.urls)),
		url(r'^$', index, name='index'),
		url(r'^posts/(?P<post_id>[0-9]+)(/$|$)', post_details, name='post_details'),
		url(r'^workouts/(?P<slug>[0-9]+)(/$|$)', WorkoutDetailView.as_view(), name='workout_details'),
		url(r'^workouts/(?P<slug>[0-9]+)/add(/$|$)', AddSetView.as_view(), name='workout_add_set', kwargs={'slug':'slug'}),
]
