
from django.test import TestCase
from mock import patch
from ui.models import Workout, ExerciseSet, Posts
from django.contrib.auth.models import User
from analysis.parsing import WorkoutLogParser, remove_tags

class PrTests(TestCase):
	
	def setUp(self):
		pass

	def test_generate_pr_entries(self):
		exerciseNames = ['Back Squat']
		
