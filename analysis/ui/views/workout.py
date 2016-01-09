from django.views.generic.detail import DetailView

from ui import models

class WorkoutDetailView(DetailView):

	model = models.Workout 
	slug_field = 'id'

	def get_template_names(self):
		return 'workout_details.html'


