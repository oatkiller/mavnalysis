from django.conf.urls import include, url
from ui import views

urlpatterns = [
		url(r'^$', views.index, name='index'),
		url(r'^posts/(?P<post_id>[0-9]+)(/$|$)', views.post_details, name='post_details'),
		url(r'^workouts/(?P<workout_id>[0-9]+)(/$|$)', views.workout_details, name='workout_details'),
]
