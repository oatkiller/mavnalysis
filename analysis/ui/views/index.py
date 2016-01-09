from django.shortcuts import render
from django.http import HttpResponse
from ui.models import Posts, Workout
from analysis.prs import get_prs

# Create your views here.
def index(request):
	repRange = range(1,6)
	logged_in_user = request.user
	context = {
		'prs' : get_prs(request=request, reps=repRange),
		'reps' : repRange,
		'workouts' : Workout.objects.order_by('-date').filter(user=logged_in_user)
	}
	return render(request, 'index.html', context)

def post_details(request, post_id):
	context = {
		'post' : Posts.objects.get(id=post_id)
	}
	return render(request, 'post_details.html', context)

class LoginView():
	
	def get_template_names(self):
		return 'login.html'
