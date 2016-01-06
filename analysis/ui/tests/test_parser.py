from django.test import TestCase
from mock import patch
from ui.models import Workout, ExerciseSet, Posts
from django.contrib.auth.models import User
from analysis.parsing import WorkoutLogParser, remove_tags

class WorkoutLogParserTests(TestCase):
	
	def setUp(self):
		User.objects.create(username='dmav')


	def test_remove_tags(self):
		text = "<strong>AM:</strong>\\nC&amp;J: Bar, 65#x2, 85x2, 95x2, 115x2, 135x2, 155x2, 175x2, 195x2, 195x1+F(clean), 155x1+2, 165x1\\n\\nCl Pull: 195x4x3\\n\\nAssorted Shoulder raises with 15, 20lbs db\\n\\n&nbsp;\\n\\nI have taken about 5 days off due to being busy, snow days, and partying. I felt out of shape today and was easily winded. I didn't feel strong and got pinned by 195lbs. I haven't gotten pinned in a clean in months. I think I must be getting sick.\\n\\n<strong>PM</strong>\\nFS+ jerk: 95x2+2, 115x2+2, 135x2+2, 165x1+2, 180x 1+1, 190x2x1+1\\nBS: 135x3, 145x3, 155x3, 165x3, 175x4x3\\nRDL: 135x5, 165x3, 180x3, 190x3x3\\nRope tri pulldowns: #4x12, #6x10, #6x8\\nPull-ups: Bwx4, 3, 3, 3\\nAb wheel rolls ankles pinned: bwx10, bwx3(free ankles)+5 pinned\\n\\nI felt that I had to finish the days workout, so I went back in and felt like a completely different man. I also drank a gallon of water between sessions mixed with emergen-C. Right lower trap/rhom was bugging me until I started lifting"
		expected_text = "AM:\\nC&amp;J: Bar, 65#x2, 85x2, 95x2, 115x2, 135x2, 155x2, 175x2, 195x2, 195x1+F(clean), 155x1+2, 165x1\\n\\nCl Pull: 195x4x3\\n\\nAssorted Shoulder raises with 15, 20lbs db\\n\\n&nbsp;\\n\\nI have taken about 5 days off due to being busy, snow days, and partying. I felt out of shape today and was easily winded. I didn't feel strong and got pinned by 195lbs. I haven't gotten pinned in a clean in months. I think I must be getting sick.\\n\\nPM\\nFS+ jerk: 95x2+2, 115x2+2, 135x2+2, 165x1+2, 180x 1+1, 190x2x1+1\\nBS: 135x3, 145x3, 155x3, 165x3, 175x4x3\\nRDL: 135x5, 165x3, 180x3, 190x3x3\\nRope tri pulldowns: #4x12, #6x10, #6x8\\nPull-ups: Bwx4, 3, 3, 3\\nAb wheel rolls ankles pinned: bwx10, bwx3(free ankles)+5 pinned\\n\\nI felt that I had to finish the days workout, so I went back in and felt like a completely different man. I also drank a gallon of water between sessions mixed with emergen-C. Right lower trap/rhom was bugging me until I started lifting"	
		self.assertEqual(expected_text,remove_tags(text))

	def test_create_single_set_with_parenthesis(self):
		text="Chin up with 3 second hang + Tricep Rope Pulldowns: BWx4+#4x10, 3x(BWx3 + #5x10)"
		mock_workout = Workout(workout_text=text)
		mock_workout.save()
		parser = WorkoutLogParser(mock_workout)
		parser.parse()
		self.assertTrue(mock_workout.sets.first().exerciseName == "Chin up with 3 second hang + Tricep Rope Pulldowns")

	def test_with_html_markup(self):
		text="Ohp: <b>62x2x5"
		mock_workout = Workout(workout_text=text)
		mock_workout.save()
		parser = WorkoutLogParser(mock_workout)
		parser.parse()
		for _set in mock_workout.sets.all():
			self.assertTrue(_set.exerciseName == "Ohp")
			self.assertTrue(_set.weight == 62)
			self.assertTrue(_set.reps == 5)

	def test_with_nonLbsOrKg_in_weight_zone(self):
		text="Banded side steps: grnx3x8\\n\\nsingle leg glute bridge: bwx3x8\\n\\nClean and Jerk: 40x2, 60x2, 60x2, 70x2, 80, 85, 90, 95, 100\\n\\nFs: 70x3, 80x3, 90x3, 100x2x2\\n\\nRdl: 90x3x4\\n\\nPause Ab wheel: bwx3x10\\nWas really able to stay upright and drive through my glutes in the front squats"
		mock_workout = Workout(workout_text=text)
		mock_workout.save()
		parser = WorkoutLogParser(mock_workout)
		parser.parse()
		# make sure no errors are thrown

	@patch.object(WorkoutLogParser,'create_single_set')
	def test_multi_set_create_sets(self, patcher):
		exercise_name = 'Bench + Accessory'
		sets = "135x5x1+6"
		mock_workout = Workout(workout_text=exercise_name + ":" + sets)
		mock_workout.save()
		w = WorkoutLogParser(mock_workout)
		w.parse()
		self.assertEqual(w.create_single_set.call_count,5)
		self.assertTrue(w.create_single_set.called_with(exercise_name,sets))

		for _call in w.create_single_set.call_list():
			self.assertEqual(_call.call_args[0],exercise_name)
			self.assertEqual(_call.call_args[1],"135x1+6")

	@patch.object(WorkoutLogParser,'create_single_set')
	def test_single_set_create_sets(self,patcher):
		mock_workout = Workout(workout_text="Bench: 225x5+2")
		mock_workout.save()
		w = WorkoutLogParser(mock_workout)
		w.parse()
		self.assertEqual(w.create_single_set.call_count,1)
		self.assertTrue(w.create_single_set.called_with("Bench","225x5+2"))

	@patch.object(WorkoutLogParser,'create_single_set')
	def test_create_sets_with_5x5x5_should_create_5_sets(self,patcher):
		mock_workout = Workout(workout_text="Bench: 225x5x5")
		mock_workout.save()
		w = WorkoutLogParser(mock_workout)
		w.parse()
		self.assertEqual(w.create_single_set.call_count,5)

	@patch.object(WorkoutLogParser,'create_single_set')
	def test_create_sets_with_5x5_should_create_1_set(self,patcher):
		mock_workout = Workout(workout_text="Bench: 225x5")
		mock_workout.save()
		w = WorkoutLogParser(mock_workout)
		w.parse()
		self.assertEqual(w.create_single_set.call_count,1)

	def test_split_lines(self):
		mock_workout = Workout()
		mock_workout.save()
		text = "Line 1 \\r\\n\\r Line 2, skip 3 \\n\\nLine 4 \\r\\n\\r Line 5"
		w = WorkoutLogParser(mock_workout)
		self.assertEqual(len(w.split_by_line(text)),5)

	@patch.object(WorkoutLogParser,'create_sets')
	def test_multi_line_parse_line(self,patcher):
		mock_workout = Workout(workout_text = "Exercise 1: 12#x5, #18x10 \\r\\n\\r Exercise 2: 2x4x3+2\\r\\n\\rComments")
		mock_workout.save()
		w = WorkoutLogParser(mock_workout)
		w.parse()
		self.assertEqual(w.create_sets.call_count,3)
		self.assertEqual(mock_workout.comments,r'\nComments')

