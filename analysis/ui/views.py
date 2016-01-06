from django.shortcuts import render
from django.http import HttpResponse
from .models import Posts, Workout
from analysis.prs import get_prs

# Create your views here.
def index(request):
	repRange = range(1,6)
	context = {
		'prs' : get_prs(request=request, reps=repRange),
		'reps' : repRange,
		'workouts' : Workout.objects.order_by('-date')
	}
	return render(request, 'index.html', context)

def post_details(request, post_id):
	context = {
		'post' : Posts.objects.get(id=post_id)
	}
	return render(request, 'post_details.html', context)

def workout_details(request, workout_id):
	context = {
		'workout' : Workout.objects.get(id=workout_id)
	}
	return render(request, 'workout_details.html', context)

