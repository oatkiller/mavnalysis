from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView
from ui.models import ExerciseSet

class AddSetView(CreateView):
	model = ExerciseSet
	fields = ['exerciseName', 'weight', 'reps', 'isLbs', 'date']

	def get_success_url(self):
		return '/'

	def get_template_names(self):
		return 'create_set.html'
